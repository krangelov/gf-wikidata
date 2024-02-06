{-# LANGUAGE CPP, MonadComprehensions, BangPatterns #-}

import Network.URI
import Network.HTTP
import Text.JSON
import Text.JSON.Types (get_field)
import Text.PrettyPrint
import OpenSSL
import qualified Data.Map as Map
import qualified Data.ByteString.Char8 as BS
import GF.Compile
import qualified GF.Data.ErrM as E
import GF.Infra.CheckM
import GF.Infra.Option
import GF.Grammar hiding ( VRecType, VApp )
import GF.Term
import System.FilePath
import Control.Applicative(liftA2)
import Control.Monad.ST.Unsafe
import Control.Monad(foldM)
import PGF2

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
      return (executeCode gr sgr mn qid lang code)

executeCode :: PGF -> SourceGrammar -> ModuleName -> String -> String -> String -> IO Response
executeCode gr sgr mn qid lang code =
  case runP pTerm (BS.pack code) of
    Right term     ->
      case runCheck (checkComputeTerm term) of
        E.Ok (value,msg)
                   -> return (Response
                                { rspCode = 200
                                , rspReason = "OK"
                                , rspHeaders = [Header HdrContentType "text/plain; charset=UTF8"]
                                , rspBody = if null msg
                                              then unlines value
                                              else unlines (msg:value)
                                })
        E.Bad msg  -> return (Response
                                { rspCode = 400
                                , rspReason = "Invalid Expression"
                                , rspHeaders = [Header HdrContentType "text/plain; charset=UTF8"]
                                , rspBody = msg
                                })
    Left (pos,msg) -> return (Response
                                { rspCode = 400
                                , rspReason = "Parse Error"
                                , rspHeaders = [Header HdrContentType "text/plain; charset=UTF8"]
                                , rspBody = (show pos ++ msg)
                                })
  where
    checkComputeTerm term = do
      let globals = Gl sgr (wikiPredef gr)
          term'   = Abs Explicit (identS "qid") term
      term' <- renameSourceTerm sgr mn term'
      (term',typ) <- checkLType globals term' (Prod Explicit identW typeStr typeStr)
      checkWarn (ppTerm Unqualified 0 term')
      checkWarn (ppTerm Unqualified 0 typ)
      normalStringForm globals (App term' (K qid))
      

wikiPredef :: PGF -> Map.Map Ident ([Value s] -> EvalM s (ConstValue (Value s)))
wikiPredef pgf = Map.fromList
  [ (identS "entity", \[typ,VStr qid] -> fetch typ qid >>= \v -> return (Const v))
  , (identS "int2digits", \[VInt n] -> int2digits abstr n >>= \v -> return (Const v))
  , (identS "int2decimal", \[VInt n] -> int2decimal abstr n >>= \v -> return (Const v))
  , (identS "float2decimal", \[VFlt f] -> float2decimal abstr f >>= \v -> return (Const v))
  , (identS "int2numeral", \[VInt n] -> int2numeral abstr n >>= \v -> return (Const v))
  , (identS "linearize", \[_,v] -> do let Just cnc = Map.lookup "ParseSwe" (languages pgf)
                                      e <- value2expr v
                                      return (Const (VStr (linearize cnc e))))
  , (cLessInt,\[v1,v2] -> return (fmap toBool (liftA2 (<) (value2int v1) (value2int v2))))
  ]
  where
    abstr = moduleNameS (abstractName pgf)

    fetch typ qid = do
      rsp <- unsafeIOToEvalM (simpleHTTP (getRequest ("https://www.wikidata.org/wiki/Special:EntityData/"++qid++".json")))
      case decode (rspBody rsp) >>= valFromObj "entities" >>= valFromObj qid >>= valFromObj "claims" of
        Ok obj    -> filterJsonFromType obj typ
        Error msg -> evalError (text msg)

    value2expr (GF.Term.VApp (_,f) tnks) = 
      foldM mkApp (EFun (showIdent f)) tnks
      where
        mkApp e1 tnk = do
          v  <- force tnk
          e2 <- value2expr v
          return (EApp e1 e2)

filterJsonFromType :: JSObject [JSObject JSValue] -> Value s -> EvalM s (Value s)
filterJsonFromType obj typ =
  case typ of
   VRecType fields -> do fields <- mapM (getSpecificProperty obj) fields
                         return (VR fields)
   _               -> evalError (text "Wikidata entities are always records")

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
  evalError (text "Wikidata entities can only have named properties")

transformJsonToTerm :: String -> Value s -> JSObject JSValue -> EvalM s Term
transformJsonToTerm field typ obj = do
  case fromJSObjectToWikiDataItem obj typ of
    Ok assign -> return (R assign)
    Error msg -> evalError (text msg)

fromJSObjectToWikiDataItem :: JSObject JSValue -> Value s -> Result [Assign]
fromJSObjectToWikiDataItem obj typ = do
  mainsnak <- valFromObj "mainsnak" obj
  datavalue <- valFromObj "datavalue" mainsnak
  validateTypeFromObj typ datavalue

validateTypeFromObj :: Value s -> JSObject JSValue -> Result [Assign]
validateTypeFromObj typ dv = do
  typFromObj <- valFromObj "type" dv
  matchTypeFromJSON dv typ typFromObj

matchTypeFromJSON :: JSObject JSValue -> Value s -> String -> Result [Assign]
matchTypeFromJSON dv (VSort id) "string" = getFieldFromString dv id
matchTypeFromJSON dv (VRecType labels) "wikibase-entityid" = traverse (getFieldFromWikibaseEntityId dv) labels
matchTypeFromJSON dv (VRecType labels) "globecoordinate" = traverse (getFieldFromGlobecoordinate dv) labels
matchTypeFromJSON dv (VRecType labels) "quantity" = traverse (getFieldFromQuantity dv) labels
matchTypeFromJSON dv (VRecType labels) "time" = traverse (getFieldFromTime dv) labels
matchTypeFromJSON dv (VRecType labels) "monolingualtext" = traverse (getFieldFromText dv) labels
matchTypeFromJSON _ _ _ = Error "Error"

getFieldFromString dv id
  | id == cStr = valFromObj "value" dv >>= \s -> return [assign theLinLabel (K s)]
  | otherwise  = fail "Not a String"

getFieldFromWikibaseEntityId dv (field@(LIdent l), t) = do
  value <- valFromObj "value" dv
  assign field
    <$> ( case (showRawIdent l, t) of
            (l@"id",  VSort id) -> if id == cStr then valFromObj l value >>= (Ok . K) else fail "Not a String"
            (_, _)              -> Error "Not a valid wikibase-entityid field"
        )

getFieldFromGlobecoordinate dv (field@(LIdent l), t) = do
  value <- valFromObj "value" dv -- globecoordinate
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
            (l@"precision",     VSort id) -> if id == cInt then valFromObj l value >>= decimal EInt else fail "Not an Int"
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
  | otherwise = evalError (text "Cant convert" <+> integer n)
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

int2decimal abstr n = int2digits abstr (abs n) >>= sign n
  where
    neg_dec = (abstr,identS "NegDecimal")
    pos_dec = (abstr,identS "PosDecimal")

    sign n t = do
      tnk <- newEvaluatedThunk t
      if n < 0
        then return (VApp neg_dec [tnk])
        else return (VApp pos_dec [tnk])

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

    range_error n = evalError (integer n <+> text "cannot be represented as a numeral")

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
