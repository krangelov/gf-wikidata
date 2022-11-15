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
  b'<p>Search for a Wikidata entity in the upper left corner!</p>'
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

    if qid:
        content.append(b'             <tr><td><a href="https://cloud.grammaticalframework.org/wikidata">Main page</a></td></tr>')
        content.append(b'             <tr><td><a href="https://www.wikidata.org/wiki/'+bytes(qid,"utf8")+b'">Wikidata item</a></td></tr>')

    content.append(b'           </table>')
    content.append(b'         </div>')

    content.append(b'         <div class="gp-panel-section">')
    content.append(b'           <h3>Languages</h3>')
    content.append(b'           <table id="from">'),
    for code,(name,cnc) in langs.items():
        if code != lang:
            if qid != None:
                content.append(bytes('             <tr><td><a href="index.wsgi?id='+qid+'&lang='+code+'">'+name+'</a></td></tr>','utf8'))
            else:
                content.append(bytes('             <tr><td><a href="index.wsgi?lang='+code+'">'+name+'</a></td></tr>','utf8'))
        else:
            content.append(bytes('             <tr><td><b>'+name+'</b></td></tr>','utf8'))
    content.append(b'         </table>')
    content.append(b'       </div>')
    content.append(b'     </div>')
    content.append(b'     <div class="gp-body" id="content" data-lang="'+bytes(lang,"utf8")+b'">')

    if qid != None:
        u2 = urllib.request.urlopen('https://www.wikidata.org/wiki/Special:EntityData/'+qid+'.json')
        result = json.loads(u2.read())
        entity = result["entities"][qid]
        cnc = gr.languages[langs[lang][1]]
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
