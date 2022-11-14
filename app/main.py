from urllib.parse import parse_qs

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

langs = {
  "afr": "Afrikaans",
  "bul": "Bulgarian",
  "cat": "Catalan",
  "chi": "Chinese",
  "dut": "Dutch",
  "eng": "English",
  "est": "Estonian",
  "fin": "Finnish",
  "fre": "French",
  "ger": "German",
  "ita": "Italian",
  "kor": "Korean",
  "mlt": "Maltese",
  "pol": "Polish",
  "por": "Portuguese",
  "ron": "Romanian",
  "rus": "Russian",
  "slo": "Slovenian",
  "som": "Somali",
  "spa": "Spanish",
  "swa": "Swahili",
  "swe": "Swedish",
  "tha": "Thai",
  "tur": "Turkish"
  }

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

    lang  = query.get("lang",["eng"])[0]
    if lang not in langs:
        lang="eng"

    content = []
    for line in prelude:
        content.append(line)
    for code,name in langs.items():
        if code != lang:
            content.append(bytes('             <tr><td><a href="index.wsgi?id='+qid+'&lang='+code+'">'+name+'</a></td></tr>','utf8'))
        else:
            content.append(bytes('             <tr><td><b>'+name+'</b></td></tr>','utf8'))

    content.append(b'         </table>')
    content.append(b'     </div>')
    content.append(b'     <div class="gp-body" id="content" data-qid="'+bytes(qid,"utf8")+b'" data-lang="'+bytes(lang,"utf8")+b'">')

    content.append(bytes(str(qid),"utf8"))
    for line in epilogue:
        content.append(line)
    return content
