import json
import html
import urllib.request
from urllib.parse import parse_qs

import pgf
gr = pgf.readNGF("/usr/local/share/x86_64-linux-ghc-8.0.2/gf-4.0.0/www/Parse.ngf")
gr.embed("wordnet")

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
  b'         <table id="from" class="gp-languages">'
  ]

concrs = gr.languages
langs = {
  "af": ("Afrikaans", concrs["ParseAfr"]),
  "bg": ("Bulgarian", concrs["ParseBul"]),
  "ca": ("Catalan",   concrs["ParseCat"]),
  "zh": ("Chinese",   concrs["ParseChi"]),
  "nl": ("Dutch",     concrs["ParseDut"]),
  "en": ("English",   concrs["ParseEng"]),
  "et": ("Estonian",  concrs["ParseEst"]),
  "fi": ("Finnish",   concrs["ParseFin"]),
  "fr": ("French",    concrs["ParseFre"]),
  "de": ("German",    concrs["ParseGer"]),
  "it": ("Italian",   concrs["ParseIta"]),
  "ko": ("Korean",    concrs["ParseKor"]),
  "mt": ("Maltese",   concrs["ParseMlt"]),
  "pl": ("Polish",    concrs["ParsePol"]),
  "pt": ("Portuguese",concrs["ParsePor"]),
  "ro": ("Romanian",  concrs["ParseRon"]),
  "ru": ("Russian",   concrs["ParseRus"]),
  "sl": ("Slovenian", concrs["ParseSlv"]),
  "so": ("Somali",    concrs["ParseSom"]),
  "es": ("Spanish",   concrs["ParseSpa"]),
  "sw": ("Swahili",   concrs["ParseSwa"]),
  "sv": ("Swedish",   concrs["ParseSwe"]),
  "th": ("Thai",      concrs["ParseTha"]),
  "tr": ("Turkish",   concrs["ParseTur"])
  }
del concrs

home = [
  b'Search for a Wikidata entity in the upper left corner.'
  ]

epilogue = [
  b'     </div>',
  b' </body>',
  b'</html>'
  ]

qids = {
  "Q89": "apple_1_N",
  "Q158657": "apple_2_N",
  "Q13099586": "pear_1_N",
  "Q434": "pear_2_N"
  }

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html; charset=utf-8')])
    query = parse_qs(env["QUERY_STRING"])
    
    qid   = query.get("id",[None])[0]
    if qid != None and (qid[0] != "Q" or not qid[1:].isdigit()):
        qid = None

    lang  = query.get("lang",["en"])[0]
    if lang not in langs:
        lang="en"

    content = []
    for line in prelude:
        content.append(line)
    for code,(name,cnc) in langs.items():
        if code != lang:
            if qid != None:
                content.append(bytes('             <tr><td><a href="index.wsgi?id='+qid+'&lang='+code+'">'+name+'</a></td></tr>','utf8'))
            else:
                content.append(bytes('             <tr><td><a href="index.wsgi?lang='+code+'">'+name+'</a></td></tr>','utf8'))
        else:
            content.append(bytes('             <tr><td><b>'+name+'</b></td></tr>','utf8'))

    content.append(b'         </table>')
    content.append(b'     </div>')
    content.append(b'     <div class="gp-body" id="content" data-lang="'+bytes(lang,"utf8")+b'">')

    if qid != None:
        u2 = urllib.request.urlopen('https://www.wikidata.org/wiki/Special:EntityData/'+qid+'.json')
        result = json.loads(u2.read())
        entity = result["entities"][qid]
        cnc = langs[lang][1]
        lex = qids.get(qid)
        if lex:
            s=cnc.linearize(pgf.ExprFun(qids[qid])).title()
        else:
            s=qid
        content.append(bytes(str("<h1>"+html.escape(s)+"</h1>"),"utf8"))
    else:
        for line in home:
            content.append(line)

    for line in epilogue:
        content.append(line)
    return content
