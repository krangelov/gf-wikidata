import json
import urllib.request
from urllib.parse import parse_qs
from daison import *

import pgf
gr = pgf.readNGF("/usr/local/share/x86_64-linux-ghc-8.0.2/gf-4.0.0/www/Parse.ngf")
gr.embed("wordnet")
import wordnet as w
from wordnet.api import *
from nlg import render
from nlg.util import *

db = openDB("/usr/local/www/gf-wordnet/semantics.db")

prelude = [
  b'<html>',
  b' <title>GFpedia</title>',
  b' <head>',
  b'     <link rel="stylesheet" type="text/css" href="gf-wikidata.css">',
  b'     <script src="gf-wikidata.js"></script>',
  b' </head>',
  b' <body>',
  b'     <div class="gp-head">',
  b'          <form class="search-box">',
  b'             <input class="search-box-input" type="search" name="search"',
  b'                    placeholder="Search GFpedia" aria-label="Search GFpedia"',
  b'                    autocapitalize="sentences" title="Search GFpedia" id="searchInput"',
  b'                    autocomplete="off"',
  b'                    oninput="showSearches(this)"',
  b'                    onkeypress="searchInputOnKeyPress(event)"',
  b'                    onkeydown="searchInputOnKeyDown(event)">',
  b'             <img class="search-box-button" src="search.svg">',
  b'             <table class="search-box-results" id="searchResults"></table>',
  b'         </form>',
  b'     </div>',
  b'     <div class="gp-panel">',
  b'         <img class="gp-logo" src="gp-logo.svg">',
  b'         <div class="gp-panel-section">',
  b'           <table>'
  ]

langs = {
  "af": ("Afrikaans", "ParseAfr"),
  "bg": ("Bulgarian", "ParseBul"),
  "ca": ("Catalan",   "ParseCat"),
  "zh": ("Chinese",   "ParseChi"),
  "nl": ("Dutch",     "ParseDut"),
  "en": ("English",   "ParseEng"),
  "et": ("Estonian",  "ParseEst"),
  "fi": ("Finnish",   "ParseFin"),
  "fr": ("French",    "ParseFre"),
  "de": ("German",    "ParseGer"),
  "it": ("Italian",   "ParseIta"),
  "ko": ("Korean",    "ParseKor"),
  "mt": ("Maltese",   "ParseMlt"),
  "pl": ("Polish",    "ParsePol"),
  "pt": ("Portuguese","ParsePor"),
  "ro": ("Romanian",  "ParseRon"),
  "ru": ("Russian",   "ParseRus"),
  "sl": ("Slovenian", "ParseSlv"),
  "so": ("Somali",    "ParseSom"),
  "es": ("Spanish",   "ParseSpa"),
  "sw": ("Swahili",   "ParseSwa"),
  "sv": ("Swedish",   "ParseSwe"),
  "th": ("Thai",      "ParseTha"),
  "tr": ("Turkish",   "ParseTur")
  }

home = [
  b'<h1>GF Pedia</h1>',
  b'<p>This is an experiment to see to what extend we can generate encyclopedic articles ',
  b'based on information from <a href="https://www.wikidata.org/">Wikidata</a> and by using ',
  b'the resource grammars in <a href="http://www.grammaticalframework.org/">GF</a> plus ',
  b'lexical resources in <a href="https://cloud.grammaticalframework.org/wordnet/">GF WordNet</a>.</p>'
  b'<p>Search for a Wikidata entity in the upper left corner.</p>'
  ]

epilogue = [
  b'     </div>',
  b' </body>',
  b'</html>'
  ]

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html; charset=utf-8')])
    query = parse_qs(env["QUERY_STRING"])
    
    qid   = query.get("id",[None])[0]
    if qid != None and (qid[0] != "Q" or not qid[1:].isdigit()):
        qid = None

    lang  = query.get("lang",["en"])[0]
    if lang not in langs:
        lang="en"

    for line in prelude:
        yield line

    if qid:
        yield b'             <tr><td><a href="https://cloud.grammaticalframework.org/wikidata">Main page</a></td></tr>'
        yield b'             <tr><td><a href="https://www.wikidata.org/wiki/'+bytes(qid,"utf8")+b'">Wikidata item</a></td></tr>'

    yield b'           </table>'
    yield b'         </div>'

    yield b'         <div class="gp-panel-section">'
    yield b'           <h3>Languages</h3>'
    yield b'           <table id="from">'
    for code,(name,cnc) in langs.items():
        if code != lang:
            if qid != None:
                yield bytes('             <tr><td><a href="index.wsgi?id='+qid+'&lang='+code+'">'+name+'</a></td></tr>','utf8')
            else:
                yield bytes('             <tr><td><a href="index.wsgi?lang='+code+'">'+name+'</a></td></tr>','utf8')
        else:
            yield bytes('             <tr><td><b>'+name+'</b></td></tr>','utf8')
    yield b'         </table>'
    yield b'       </div>'
    yield b'     </div>'
    yield b'     <div class="gp-body" id="content" data-lang="'+bytes(lang,"utf8")+b'">'

    if qid != None:
        u2 = urllib.request.urlopen('https://www.wikidata.org/wiki/Special:EntityData/'+qid+'.json')
        result = json.loads(u2.read())
        entity = result["entities"][qid]
        cnc = gr.languages[langs[lang][1]]

        lex_fun = get_lex_fun(db, qid)
        if lex_fun:
            for s in render(db,lex_fun,cnc,entity):
                yield bytes(s,"utf8")
        else:
            yield bytes("<h1>"+qid+"</h1>","utf8")
            yield bytes("<p>There is no NLG for this item yet.</p>","utf8")
    else:
        for line in home:
            yield line

    for line in epilogue:
        yield line
