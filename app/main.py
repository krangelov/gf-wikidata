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

def prelude(qid,lang,edit):
  yield b'<html>'
  yield b' <title>GFpedia</title>'
  yield b' <head>'
  yield b'     <link rel="stylesheet" type="text/css" href="../wordnet/gf-wordnet.css">'
  yield b'     <link rel="stylesheet" type="text/css" href="gf-wikidata.css">'
  yield b'     <script src="/js/support.js"></script>'
  yield b'     <script src="https://unpkg.com/vis-network@9.0.4/standalone/umd/vis-network.min.js"></script>'
  yield b'     <script src="../wordnet/js/gf-wordnet.js"></script>'
  yield b'     <script src="../wordnet/js/wordcloud2.js"></script>'
  yield b'     <script src="gf-wikidata.js"></script>'
  yield b' </head>'
  if edit:
    yield b' <body onload="init_editor()">'
  else:
    yield b' <body>'
  yield b'     <div class="gp-head">'

  if qid:
    yield b'<ul class="gp-navigation">'
    if edit:
        yield b'<li><a href="index.wsgi?id='+bytes(qid,"utf-8")+b'&lang='+bytes(lang,"utf-8")+b'">Page</a></li><li class="selected">Edit</li>'
    else:
        yield b'<li class="selected">Page</li><li><a href="index.wsgi?id='+bytes(qid,"utf-8")+b'&lang='+bytes(lang,"utf-8")+b'&edit=1">Edit</a></li>'  
    yield b'</ul>'

  yield b'          <form class="search-box">'
  yield b'             <input class="search-box-input" type="search" name="search"'
  yield b'                    placeholder="Search GFpedia" aria-label="Search GFpedia"'
  yield b'                    autocapitalize="sentences" title="Search GFpedia" id="searchInput"'
  yield b'                    autocomplete="off"'
  yield b'                    oninput="showSearches(this)"'
  yield b'                    onkeypress="searchInputOnKeyPress(event)"'
  yield b'                    onkeydown="searchInputOnKeyDown(event)">'
  yield b'             <img class="search-box-button" src="search.svg">'
  yield b'             <table class="search-box-results" id="searchResults"></table>'
  yield b'         </form>'
  yield b'     </div>'
  yield b'     <div class="gp-panel">'
  yield b'         <img class="gp-logo" src="gp-logo.svg">'
  yield b'         <div class="gp-panel-section">'
  yield b'           <table>'

  if qid:
    yield b'             <tr><td><a href="https://cloud.grammaticalframework.org/wikidata">Main page</a></td></tr>'
    yield b'             <tr><td><a href="https://www.wikidata.org/wiki/'+bytes(qid,"utf8")+b'">Wikidata item</a></td></tr>'

  yield b'           </table>'
  yield b'         </div>'

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
  b'<h1 class="gp-page-title">GF Pedia</h1>',
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

    edit = query.get("edit",["0"])[0]=="1"

    for line in prelude(qid,lang,edit):
        yield line

    yield b'         <div class="gp-panel-section">'
    yield b'           <h3 class="gp-page-title">Languages</h3>'
    yield b'           <table id="from">'
    for code,(name,cnc) in langs.items():
        yield b'             <tr>'
        if code != lang:
            if qid != None:
                if edit:
                    yield bytes('<td><a href="index.wsgi?id='+qid+'&lang='+code+'&edit=1">'+name+'</a></td>','utf8')
                else:
                    yield bytes('<td><a href="index.wsgi?id='+qid+'&lang='+code+'">'+name+'</a></td>','utf8')
            else:
                yield bytes('<td><a href="index.wsgi?lang='+code+'">'+name+'</a></td>','utf8')
        else:
            yield bytes('<td><b>'+name+'</b></td>','utf8')
        if edit:
            yield bytes('<td><input type="checkbox" name="'+cnc+'" onchange="select_language()"></td>','utf8')
        yield b'</tr>'
    yield b'         </table>'
    yield b'       </div>'
    yield b'     </div>'
    yield b'     <div class="gp-body" id="content" data-lang="'+bytes(lang,"utf8")+b'">'

    if qid != None:
        u2 = urllib.request.urlopen('https://www.wikidata.org/wiki/Special:EntityData/'+qid+'.json')
        result = json.loads(u2.read())
        entity = result["entities"][qid]
        cnc = ConcrHelper(gr.languages[langs[lang][1]],db,lang,edit)

        lex_fun = cnc.get_lex_fun(qid,link=False)
        if not lex_fun:
            given_names  = cnc.get_lexemes("P735",entity,qual=False,link=False)
            family_names = cnc.get_lexemes("P734",entity,qual=False,link=False)
            if given_names:
                if family_names:
                    lex_fun=w.FullName(given_names[0],family_names[0])
                else:
                    lex_fun=w.GivenName(given_names[0])
            else:
                if family_names:
                    lex_fun=w.Surname(family_names[0])

        if lex_fun:
            for s in render(cnc,lex_fun,entity):
                yield bytes(s,"utf8")
        else:
            yield bytes('<h1 class="gp-page-title">'+qid+"</h1>","utf8")
            yield bytes("<p>There is no NLG for this item yet.</p>","utf8")

        if cnc.exprs:
            yield b'<div class="gp-dump">'
            for e in cnc.exprs:
                yield bytes("<p>"+str(e)+"</p>","utf8")
            yield b"</div>"
    else:
        for line in home:
            yield line

    for line in epilogue:
        yield line
