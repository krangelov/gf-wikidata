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
  [ (identS "entity",    \[typ,VStr qid] -> fetch typ qid >>= \v -> return (Const v))
  , (identS "linearize", \[_,v] -> do let Just cnc = Map.lookup "ParseSwe" (languages pgf)
                                      e <- value2expr v
                                      return (Const (VStr (linearize cnc e))))
  ]
  where
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
  | otherwise  = Error "Not a String"

getFieldFromWikibaseEntityId dv (field@(LIdent l), t) = do
  value <- valFromObj "value" dv
  assign field
    <$> ( case (showRawIdent l, t) of
            (l@"id",  VSort id) -> if id == cStr then valFromObj l value >>= (Ok . K) else Error "Not a String"
            (_, _)              -> Error "Not a valid field for type wikibase-entityid"
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
            (_, _)                     -> Error "Not a valid field for type globecoordinate"
        )

getFieldFromQuantity dv (field@(LIdent l), t) = do
  value <- valFromObj "value" dv -- quantity
  assign field
    <$> ( case (showRawIdent l, t) of
            (l@"amount", VApp f []) -> if f == (cPredef,cInt)
                                        then valFromObj l value >>= decimal EInt
                                        else if f == (cPredef,cFloat)
                                               then valFromObj l value >>= decimal EFloat
                                               else fail "Not an Int or Float"
            (l@"unit", VSort id)    -> if id == cStr            then K . dropURL <$> valFromObj l value    else fail "Not a String"
            (_, _)                  -> fail "Not a valid field for type quantity"
        )

getFieldFromTime dv (field@(LIdent l), t) = do
  value <- valFromObj "value" dv -- time
  assign field
    <$> ( case (showRawIdent l, t) of
            (l@"time",          VSort id) -> if id == cStr then valFromObj l value >>= (Ok . K) else fail "Not a String"
            (l@"precision",     VSort id) -> if id == cInt then valFromObj l value >>= decimal EInt else fail "Not an Int"
            (l@"calendarmodel", VSort id) -> if id == cStr then K . dropURL <$> valFromObj l value else fail "Not a String"
            (_, _)                        -> fail "Not a valid field"
        )

getFieldFromText dv (field@(LIdent l), t) = do
  value <- valFromObj "value" dv -- monolingualtext
  assign field
    <$> ( case (showRawIdent l, t) of
            (l@"text",     VSort id) -> if id == cStr then valFromObj l value >>= (Ok . K) else Error "Not a String"
            (l@"language", VSort id) -> if id == cStr then valFromObj l value >>= (Ok . K) else Error "Not a String"
            (_, _)                   -> Error "Not a valid field"
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
