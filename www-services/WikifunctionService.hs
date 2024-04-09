{-# LANGUAGE CPP                 #-}
{-# LANGUAGE MonadComprehensions #-}

import Control.Applicative     (liftA2, (<|>))
import Control.Monad           (foldM, filterM, liftM2, mzero)
import Control.Monad.ST.Unsafe
import qualified Data.ByteString.Char8   as BS
import qualified Data.Map                as Map
import GF.Compile
import qualified GF.Data.ErrM            as E
import GF.Grammar              hiding (VApp, VRecType)
import GF.Grammar.Lookup
import GF.Infra.CheckM
import GF.Infra.Option
import GF.Term
import GF.Compile.Rename
import Network.HTTP
import Network.HTTP.MD5
import Network.URI
import OpenSSL
import PGF2
import System.IO ( utf8 )
import System.FilePath
import Text.JSON
import Text.JSON.Types         (get_field)
import GF.Text.Pretty

import qualified Data.Text.Lazy as TL
import qualified Data.Text.Lazy.Encoding as E
import qualified Data.ByteString.Lazy as BL

import            Data.Maybe
main = do
  gr <- readNGF "/usr/local/share/x86_64-linux-ghc-8.8.4/gf-4.0.0/www/robust/Parse.ngf"
  (_,(mn,sgr)) <- batchCompile noOptions (Just gr) ["WordNet.gf"]
  withOpenSSL (simpleServer (Just 8080) Nothing (httpMain gr sgr mn))


httpMain :: PGF -> SourceGrammar -> ModuleName -> Request -> IO Response
httpMain gr sgr mn rq
  | takeExtension path == ".html" = do
      print path
      html <- readFile ("../www"++path)
      return (Response
                { rspCode = 200
                , rspReason = "OK"
                , rspHeaders = [Header HdrContentType "text/html; charset=UTF8"]
                , rspBody = html
                })
  | takeExtension path == ".js" = do
      print path
      code <- readFile ("../www"++path)
      return (Response
                { rspCode = 200
                , rspReason = "OK"
                , rspHeaders = [Header HdrContentType "application/json; charset=UTF8"]
                , rspBody = code
                })
  | path == "/execute" =
      case decode (rqBody rq) >>= parseQuery of
        Ok f      -> f
        Error msg -> return (Response
                               { rspCode = 400
                               , rspReason = "Invalid input"
                               , rspHeaders = [Header HdrContentType "text/plain; charset=UTF8"]
                               , rspBody = msg
                               })
  | otherwise    =  return (Response
                               { rspCode = 400
                               , rspReason = "Not found"
                               , rspHeaders = []
                               , rspBody = ""
                               })
  where
    path = uriPath (rqURI rq)

    parseQuery query = do
      qid  <- valFromObj "qid"  query
      lang <- valFromObj "lang" query
      code <- valFromObj "code" query
      return (executeCode gr sgr mn "" qid lang code)

executeCode :: PGF -> SourceGrammar -> ModuleName -> String -> String -> String -> String -> IO Response
executeCode gr sgr mn cwd qid lang code =
  case runLangP NLG pNLG (BS.pack code) of
    Right prog ->
      case runCheck (checkComputeProg prog) of
        E.Ok ((headers,dataset),msg)
                   -> return (Response
                                { rspCode = 200
                                , rspReason = "OK"
                                , rspHeaders = [Header HdrContentType "application/json; charset=UTF8"]
                                , rspBody = encode $
                                              makeObj [("msg",showJSON msg),
                                                       ("headers",showJSON headers),
                                                       ("dataset",showJSON dataset)]
                                })
        E.Bad msg  -> return (Response
                                { rspCode = 400
                                , rspReason = "Invalid Expression"
                                , rspHeaders = [Header HdrContentType "text/plain; charset=UTF8"]
                                , rspBody = msg
                                })
    Left (Pn row col,msg)
                   -> return (Response
                                { rspCode = 400
                                , rspReason = "Parse Error"
                                , rspHeaders = [Header HdrContentType "text/plain; charset=UTF8"]
                                , rspBody = (show row ++ ":" ++ show col ++ ":" ++ msg)
                                })
  where
    abs_mn = moduleNameS (abstractName gr)

    checkComputeProg jments = do
      let nlg_mn = moduleNameS (msrc nlg_mi)
          nlg_mi = ModInfo {
                     mtype   = MTResource,
                     mstatus = MSComplete,
                     mflags  = noOptions,
                     mextend = [],
                     mwith   = Nothing,
                     mopens  = [OSimple mn, OSimple abs_mn],
                     mexdeps = [],
                     msrc    = "<NLG module>",
                     mseqs   = Nothing,
                     jments  = jments
                   }
      nlg_m <- renameModule cwd sgr (nlg_mn, nlg_mi)

      infoss <- checkInModule cwd nlg_mi NoLoc empty $ topoSortJments2 nlg_m
      let sgr'    = prependModule sgr nlg_m
          globals = Gl sgr (wikiPredef gr)
      nlg_m <- foldM (foldM (checkInfo (mflags nlg_mi) cwd globals)) nlg_m infoss

      let sgr' = prependModule sgr nlg_m
          globals' = Gl sgr' (wikiPredef gr)
          qident = (nlg_mn,identS "main")

      term' <- lookupResDef  sgr' qident
      ty    <- lookupResType sgr' qident

      checkWarn (ppTerm Unqualified 0 term')

      let (_,res_ty) = typeFormCnc ty

      t <- normalForm globals' (App (App term' Empty) (K qid))
      return (toHeaders res_ty, toDataset res_ty t)

    toHeaders (RecType lbls) = [render (pp l <+> ':' <+> ppTerm Unqualified 0 ty) | (l,ty) <- lbls]
    toHeaders ty             = [render (ppTerm Unqualified 0 ty)]

    toDataset ty (FV ts) = ts >>= toRecord ty
    toDataset ty t       = toRecord ty t

    toRecord (RecType lbls) (R as) = toCells lbls as
    toRecord ty             t      = [[c] | c <- toCell ty t]

    toCells []            as = return []
    toCells ((l,ty):lbls) as =
      case lookup l as of
        Just (_,t) -> do c  <- toCell ty t
                         cs <- toCells lbls as
                         return (c:cs)
        Nothing    -> toCells lbls as

    toCell (Sort s)  t
      | s == cStr =
          case toStr t of
            Just s  -> return s
            Nothing -> return (render (ppTerm Unqualified 0 t))
    toCell (QC (m,c)) t
      | m == abs_mn    = let Just cnc = Map.lookup "ParseEng" (languages gr)
                         in fmap (linearize cnc) (toExpr t)
    toCell ty        t = return (render (ppTerm Unqualified 0 t))

    toExpr (App t1 t2) = liftM2 EApp (toExpr t1) (toExpr t2)
    toExpr (QC (_,c))  = return (EFun (showIdent c))
    toExpr (EInt n)    = return (ELit (LInt n))
    toExpr (EFloat d)  = return (ELit (LFlt d))
    toExpr (ImplArg t) = fmap EImplArg (toExpr t)
    toExpr (Meta i)    = return (EMeta i)
    toExpr (FV ts)     = ts >>= toExpr
    toExpr t           = case toStr t of
                           Just s  -> return (ELit (LStr s))
                           Nothing -> mzero

    toStr (K s)        = Just s
    toStr (C t1 t2)    = do s1 <- toStr t1
                            s2 <- toStr t2
                            return (s1 ++ " " ++ s2)
    toStr (Glue t1 t2) = do s1 <- toStr t1
                            s2 <- toStr t2
                            return (s1 ++ s2)
    toStr _            = Nothing

    checkInfo :: Options -> FilePath -> Globals -> SourceModule -> (Ident,Info) -> Check SourceModule
    checkInfo opts cwd globals sm (c,info) = checkInModule cwd (snd sm) NoLoc empty $ do
       case info of
         ResOper pty pde -> do
            (pty', pde') <- case (pty,pde) of
                (Just (L loct ty), Just (L locd de)) -> do
                     ty'     <- chIn loct "operation" $ do
                                   (ty,_) <- checkLType globals ty typeType
                                   normalForm globals ty
                     (de',_) <- chIn locd "operation" $
                                   checkLType globals de ty'
                     return (Just (L loct ty'), Just (L locd de'))
                (Nothing         , Just (L locd de)) -> do
                     (de',ty') <- chIn locd "operation" $
                                     inferLType globals de
                     return (Just (L locd ty'), Just (L locd de'))
                (Just (L loct ty), Nothing) -> do
                     chIn loct "operation" $
                        checkError (pp "No definition given to the operation")
            update sm c (ResOper pty' pde')
       where
         gr = prependModule sgr sm
         chIn loc cat = checkInModule cwd (snd sm) loc ("Happened in" <+> cat <+> c)

         update (mn,mi) c info = return (mn,mi{jments=Map.insert c info (jments mi)})

wikiPredef :: PGF -> Map.Map Ident ([Value s] -> EvalM s (ConstValue (Value s)))
wikiPredef pgf = Map.fromList
  [ (identS "entity", \[typ,VStr qid] -> fetch typ qid >>= \v -> return (Const v))
  , (identS "int2digits", \[VInt n] -> int2digits abstr n >>= \v -> return (Const v))
  , (identS "int2decimal", \[VInt n] -> int2decimal abstr n >>= \v -> return (Const v))
  , (identS "float2decimal", \[VFlt f] -> float2decimal abstr f >>= \v -> return (Const v))
  , (identS "int2numeral", \[VInt n] -> int2numeral abstr n >>= \v -> return (Const v))
  , (identS "markup", \[_, tag, attrs, v] -> markup' tag attrs v)
  , (identS "linearize", linearize')
  , (cLessInt,\[v1,v2] -> return (fmap toBool (liftA2 (<) (value2int v1) (value2int v2))))
  ]
  where
    abstr = moduleNameS (abstractName pgf)

    fetch typ qid = do
      rsp <- unsafeIOToEvalM (simpleHTTP (getRequest ("https://www.wikidata.org/wiki/Special:EntityData/"++qid++".json")))
      case decode (rspBody rsp) >>= valFromObj "entities" >>= valFromObj qid >>= valFromObj "claims" of
        Ok obj    -> filterJsonFromType obj typ
        Error msg -> evalError (pp msg)

    value2expr (GF.Term.VApp (_,f) tnks) =
      foldM mkApp (EFun (showIdent f)) tnks
      where
        mkApp e1 tnk = do
          v  <- force tnk
          e2 <- value2expr v
          return (EApp e1 e2)
    
    linearize' :: [Value s] -> EvalM s (ConstValue (Value s))
    linearize' [_, GF.Term.VInt n] = return (Const (VStr (show n)))
    linearize' [_, GF.Term.VStr s] = return (Const (VStr (concatMap escape s)))
    linearize' [_, GF.Term.VEmpty] = return (Const (VStr ""))
    linearize' [_, GF.Term.VR [(_, tnk)]] =
      do
        v  <- force tnk
        return (Const v)
    linearize' [x, GF.Term.VC v1 v2] =
      do
        (Const (VStr s1)) <- linearize' [x, v1]
        (Const (VStr s2)) <- linearize' [x, v2]
        return (Const (VStr (s1 ++ s2)))
    linearize' [_, v] = do
                          let Just cnc = Map.lookup "ParseEng" (languages pgf)
                          e <- value2expr  v
                          return (Const (VStr (concatMap escape (linearize cnc e))))

    markup' (VStr tag) (VR attrs) VEmpty = 
      do
        attrs' <- constructAttrs attrs
        return (Const 
                (VStr
                  (constructHtml tag (Just "") attrs')))
    markup' (VStr tag) (VR attrs) (VStr v) = 
      do
        attrs' <- constructAttrs attrs
        return (Const
                (VStr
                  (constructHtml tag Nothing attrs')))
    markup' (VR attrs)  (VStr tag) (VStr v) =
      do
        attrs' <- constructAttrs attrs
        return (Const
                (VStr
                  (constructHtml tag (Just v) attrs')))
    markup' (VR attrs)  (VStr tag) vc@(VC _ _) =
      do
        attrs' <- constructAttrs attrs
        return (Const
                (VStr
                  (constructHtml tag (constructFromConcat vc) attrs')))
    markup' attrs tag v = evalError (pp "Invalid markup")

constructFromConcat :: Value s -> Maybe String
constructFromConcat (VStr v) = Just v
constructFromConcat VEmpty = Nothing
constructFromConcat (VC v1 v2) = case constructFromConcat v1 of
                                    Just str -> Just (str ++ Data.Maybe.fromMaybe "" (constructFromConcat v2))
                                    Nothing -> constructFromConcat v2
constructFromConcat v = Nothing

constructAttrs :: [(Label, Thunk s)] -> EvalM s [(String, String)]
constructAttrs [] = return []
constructAttrs ((LIdent l, v) : attrs) = do
  VStr v' <- force v
  vs <- constructAttrs attrs
  return ((showRawIdent l, v') : vs)

constructHtml :: String -> Maybe String -> [(String, String)] -> String
constructHtml name payload attrs = "<" ++ name ++ " " ++ unwords (go attrs) ++ ">" ++ payload'
      where go [] = [ "" ]
            go ((lbl, val) : attrs) = (lbl ++ "=" ++ "\"" ++ concatMap escape val ++ "\"") : go attrs
            payload' = case payload of
                         Nothing -> ""
                         Just payload -> payload ++ "</" ++ name ++ ">"

escape '<' = "&lt;"
escape '>' = "&gt;"
escape '&' = "&amp;"
escape '"' = "&quot;"
escape c   = [c]

filterJsonFromType :: JSObject [JSObject JSValue] -> Value s -> EvalM s (Value s)
filterJsonFromType obj typ =
  case typ of
   VRecType fields -> do fields <- mapM (getSpecificProperty obj) fields
                         return (VR fields)
   _               -> evalError (pp "Wikidata entities are always records")

getSpecificProperty :: JSObject [JSObject JSValue] -> (Label, Value s) -> EvalM s (Label, Thunk s)
getSpecificProperty obj (LIdent field, typ) =
  case Text.JSON.Types.get_field obj label of
    Nothing   -> do tnk <- newThunk [] (FV [])
                    return (LIdent field, tnk)
    Just objs -> do terms <- mapM (transformJsonToTerm label typ) objs
                    tnk <- newThunk [] (FV terms)
                    return (LIdent field, tnk)
  where
    label = showRawIdent field
getSpecificProperty obj (LVar n, typ) =
  evalError (pp "Wikidata entities can only have named properties")

transformJsonToTerm :: String -> Value s -> JSObject JSValue -> EvalM s Term
transformJsonToTerm field typ obj =
  case typ of
      VRecType [(LIdent l, t)] | head (showRawIdent l) == 'P'  -> case getCorrectObject obj t (showRawIdent l) of
                                                                    Ok assign -> return (R [(LIdent l , (Nothing, R assign))])
                                                                    Error "Could not find the correct object" -> return (FV [])
                                                                    Error msg -> evalError (pp msg)

      _                                                        -> case fromJSObjectToWikiDataItem obj typ of
                                                                    Ok assign -> return (R assign)
                                                                    Error msg -> evalError (pp msg)

getCorrectObject obj typ l = do
  let qualifiers = (do
                      qualifiers <- valFromObj "qualifiers" obj
                      valFromObj l qualifiers
                    )

  let references = (do
                      references  <- valFromObj "references" obj
                      references' <- valFromObj "snaks" (head references)
                      valFromObj l references'
                    )

  case qualifiers <|> references of
    Ok specific -> do
                      datavalue  <- valFromObj "datavalue" (head specific)
                      datatype  <- valFromObj "datatype" (head specific)
                      validateTypeFromObj typ datavalue datatype
    Error msg   -> Error "Could not find the correct object"


fromJSObjectToWikiDataItem :: JSObject JSValue -> Value s -> Result [Assign]
fromJSObjectToWikiDataItem obj typ = do
  mainsnak <- valFromObj "mainsnak" obj
  datatype <- valFromObj "datatype" mainsnak
  datavalue <- valFromObj "datavalue" mainsnak
  validateTypeFromObj typ datavalue datatype

validateTypeFromObj :: Value s -> JSObject JSValue -> String -> Result [Assign]
validateTypeFromObj typ dv  datatype = 
  case matchTypeFromJSON dv typ datatype of
    Ok assign -> return assign
    Error msg -> Error msg

matchTypeFromJSON ::  JSObject JSValue -> Value s -> String -> Result [Assign]
matchTypeFromJSON  dv (VRecType labels) "commonsMedia" = traverse (getFieldFromCommonsMedia dv) labels
matchTypeFromJSON  dv (VRecType labels) "quantity" = traverse (getFieldFromQuantity dv) labels
matchTypeFromJSON dv (VRecType labels) "wikibase-item" = traverse (getFieldFromWikibaseEntityId dv) labels
matchTypeFromJSON dv (VRecType labels) "globe-coordinate" = traverse (getFieldFromGlobecoordinate dv) labels
matchTypeFromJSON  dv (VRecType labels) "time" = traverse (getFieldFromTime dv) labels
matchTypeFromJSON dv (VRecType labels) "monolingualtext" = traverse (getFieldFromText dv) labels
matchTypeFromJSON _ v t = Error $ "Error" ++ showValue v ++ t


getFieldFromCommonsMedia :: JSObject JSValue -> (Label, Value s) -> Result Assign
getFieldFromCommonsMedia dv (LIdent l, t) =
  case (showRawIdent l, t) of 
      ("s", VSort id) -> if id == cStr then valFromObj "value" dv >>= \s -> return $ assign theLinLabel (K (constructImgUrl s)) else fail "Not a String"
      ("s", VMeta _ _) -> valFromObj "value" dv >>= \s -> return $ assign theLinLabel (K (constructImgUrl s))
      (_, _) -> Error "Not a valid commons-media field"


constructImgUrl :: String -> String
constructImgUrl img =
  let
    name = map (\c -> if c == ' ' then '_' else c) (unEscapeString img)
    h    = md5ss utf8 name    
  in "https://upload.wikimedia.org/wikipedia/commons/"++take 1 h++"/"++take 2 h++"/"++name

getFieldFromWikibaseEntityId dv (field@(LIdent l), t) = do
  value <- valFromObj "value" dv
  assign field
    <$> ( case (showRawIdent l, t) of
            (l@"id",  VSort id) -> if id == cStr then valFromObj l value >>= (Ok . K) else fail "Not a String"
            (l@"id",  VMeta _ _) -> valFromObj l value >>= (Ok . K)

            (_, _)              -> Error "Not a valid wikibase-entityid field"
        )

getFieldFromGlobecoordinate dv (field@(LIdent l), t) = do
  value <- valFromObj "value" dv
  assign field
    <$> ( case (showRawIdent l, t) of
            (l@"latitude",  VApp f []) -> if f == (cPredef,cFloat) then valFromObj l value >>= (Ok . EFloat) else fail "Not a Float"
            (l@"longitude", VApp f []) -> if f == (cPredef,cFloat) then valFromObj l value >>= (Ok . EFloat) else fail "Not a Float"
            (l@"precision", VApp f []) -> if f == (cPredef,cFloat) then valFromObj l value >>= (Ok . EFloat) else fail "Not a Float"
            (l@"altitude",  VApp f []) -> if f == (cPredef,cFloat) then valFromObj l value >>= (Ok . EFloat) else fail "Not a Float"
            (l@"globe",     VSort id)  -> if id == cStr            then valFromObj l value >>= (Ok . K)      else fail "Not a String"
            (_, _)                     -> Error "Not a valid globecoordinates field"
        )

getFieldFromQuantity dv (field@(LIdent l), t) = do
  value <- valFromObj "value" dv -- quantity
  assign field
    <$> ( case (showRawIdent l, t) of
            (l@"amount", VApp f [])
              | f == (cPredef,cInt)   -> valFromObj l value >>= decimal EInt
              | f == (cPredef,cFloat) -> valFromObj l value >>= decimal EFloat
              | otherwise             -> fail "Not an Int or Float"
            (l@"unit", VSort id)      -> if id == cStr            then K . dropURL <$> valFromObj l value    else fail "Not a String"
            (_, _)                    -> fail "Not a valid quantity field"
        )

getFieldFromTime dv (field@(LIdent l), t) = do
  value <- valFromObj "value" dv -- time
  assign field
    <$> ( case (showRawIdent l, t) of
            (l@"time",          VSort id) -> if id == cStr then valFromObj l value >>= (Ok . K) else fail "Not a String"
            (l@"precision",     VApp f []) -> if f == (cPredef, cInt) then EInt <$> valFromObj l value else fail "Not an Int"
            (l@"calendarmodel", VSort id) -> if id == cStr then K . dropURL <$> valFromObj l value else fail "Not a String"
            (_, _)                        -> fail "Not a valid time field"
        )

getFieldFromText dv (field@(LIdent l), t) = do
  value <- valFromObj "value" dv -- monolingualtext
  assign field
    <$> ( case (showRawIdent l, t) of
            (l@"text",     VSort id) -> if id == cStr then valFromObj l value >>= (Ok . K) else fail "Not a String"
            (l@"language", VSort id) -> if id == cStr then valFromObj l value >>= (Ok . K) else fail "Not a String"
            (_, _)                   -> fail "Not a valid text field"
        )

dropURL s = match "http://www.wikidata.org/entity/" s
  where
    match [] ys = ys
    match (x : xs) (y : ys)
      | x == y = match xs ys
    match _ _ = s

decimal c ('+' : s) = decimal c s
decimal c s =
  case reads s of
    [(v, "")] -> return (c v)
    _         -> fail "Not a decimal"

int2digits abstr n
  | n >= 0    = digits n
  | otherwise = evalError (pp "Can't convert" <+> pp n)
  where
    idig    = (abstr,identS "IDig")
    iidig   = (abstr,identS "IIDig")

    digit n = (VApp (abstr,identS ('D':'_':show n)) [])

    digits n = do
      let (n2,n1) = divMod n 10
      tnk <- newEvaluatedThunk (digit n1)
      rest n2 (VApp idig [tnk])

    rest 0 t = return t
    rest n t = do
      let (n2,n1) = divMod n 10
      tnk1 <- newEvaluatedThunk (digit n1)
      tnk2 <- newEvaluatedThunk t
      rest n2 (VApp iidig [tnk1, tnk2])

int2decimal :: ModuleName -> Integer -> EvalM s (Value s)
int2decimal abstr n = int2digits abstr (abs n) >>= sign n
  where
    neg_dec = (abstr,identS "NegDecimal")
    pos_dec = (abstr,identS "PosDecimal")

    sign n t = do
      tnk <- newEvaluatedThunk t
      if n < 0
        then return (VApp neg_dec [tnk])
        else return (VApp pos_dec [tnk])

float2decimal :: ModuleName -> Double -> EvalM s (Value s)
float2decimal abstr f =
  let n = truncate f
  in int2decimal abstr n >>= fractions (f-fromIntegral n)
  where
    ifrac = (abstr,identS "IFrac")

    digit n = (VApp (abstr,identS ('D':'_':show n)) [])

    fractions f t
      | f < 1e-8  = return t
      | otherwise = do
          let f10 = f * 10
              n2  = truncate f10
          tnk1 <- newEvaluatedThunk t
          tnk2 <- newEvaluatedThunk (digit n2)
          fractions (f10-fromIntegral n2) (VApp ifrac [tnk1, tnk2])

int2numeral abstr n
  | n < 1000000000000 = n2s1000000000000 n >>= app1 "num"
  | otherwise         = range_error n
  where
    n2s1000000000000 n
      | n < 1000000000 = n2s1000000000 n >>= app1 "pot4as5"
      | otherwise      = let (n1,n2) = divMod n 1000000000
                         in if n2 == 0
                            then n2s1000 n1 >>= app1 "pot5"
                            else do n1 <- n2s1000       n1
                                    n2 <- n2s1000000000 n2
                                    app2 "pot5plus" n1 n2

    n2s1000000000 n
      | n < 1000000 = n2s1000000 n >>= app1 "pot3as4"
      | otherwise   = let (n1,n2) = divMod n 1000000
                      in if n2 == 0
                           then n2s1000 n1 >>= app1 "pot4"
                           else do n1 <- n2s1000    n1
                                   n2 <- n2s1000000 n2
                                   app2 "pot4plus" n1 n2

    n2s1000000 n
      | n < 1000  = n2s1000 n >>= app1 "pot2as3"
      | otherwise = let (n1,n2) = divMod n 1000
                    in if n2 == 0
                         then n2s1000 n1 >>= app1 "pot3"
                         else do n1 <- n2s1000 n1
                                 n2 <- n2s1000 n2
                                 app2 "pot3plus" n1 n2

    n2s1000 n
      | n < 100   = n2s100 n >>= app1 "pot1as2"
      | otherwise = let (n1,n2) = divMod n 100
                    in if n2 == 0
                         then n2s10 n1 >>= app1 "pot2"
                         else do n1 <- n2s10  n1
                                 n2 <- n2s100 n2
                                 app2 "pot2plus" n1 n2

    n2s100 n
      | n <  10   = n2s10 n >>= app1 "pot0as1"
      | n == 10   = return (VApp (abstr,identS "pot110") [])
      | n == 11   = return (VApp (abstr,identS "pot111") [])
      | n <  20   = n2d (n-10) >>= app1 "pot1to19"
      | otherwise = let (n1,n2) = divMod n 10
                    in if n2 == 0
                         then n2d n1 >>= app1 "pot1"
                         else do n1 <- n2d   n1
                                 n2 <- n2s10 n2
                                 app2 "pot1plus" n1 n2

    n2s10 n
      | n < 1     = range_error n
      | n == 1    = return (VApp (abstr,identS "pot01") [])
      | otherwise = n2d n >>= app1 "pot0"

    n2d n = app0 ('n':show n)

    range_error n = evalError (pp n <+> pp "cannot be represented as a numeral")

    app0 fn = return (VApp (abstr,identS fn) [])

    app1 fn v1 = do
      tnk1 <- newEvaluatedThunk v1
      return (VApp (abstr,identS fn) [tnk1])

    app2 fn v1 v2 = do
      tnk1 <- newEvaluatedThunk v1
      tnk2 <- newEvaluatedThunk v2
      return (VApp (abstr,identS fn) [tnk1,tnk2])


value2int (VInt n) = Const n
value2int _        = RunTime

toBool True  = VApp (cPredef,identS "True")  []
toBool False = VApp (cPredef,identS "False") []
