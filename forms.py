import bz2
import json
import urllib.request


lexicon  = {}
langs    = {}
tags     = {}
features = {}

with bz2.BZ2File("../Downloads/latest-lexemes.json.bz2", "r") as source_file:
    for line in source_file:
        line = line.decode("utf-8").strip()
        if line=="[" or line=="]":
            continue
        if line[-1] == ",":
            line = line[:-1]

        try:
            lexeme = json.loads(line)
        except json.decoder.JSONDecodeError as e:
            print(line)
            raise e

        qlang = lexeme["language"]
        lang = langs.get(qlang)
        if lang == None:
            contents = urllib.request.urlopen("https://www.wikidata.org/wiki/Special:EntityData/"+qlang+".json").read().decode("utf-8")
            entity = json.loads(contents)["entities"][qlang]
            if "P220" in entity["claims"] and "datavalue" in entity["claims"]["P220"][0]["mainsnak"]:
                lang = entity["claims"]["P220"][0]["mainsnak"]["datavalue"]["value"]
            else:
                lang = qlang
            langs[qlang] = lang

        qtag = lexeme["lexicalCategory"]
        tag  = tags.get(qtag)
        if tag == None:
            contents = urllib.request.urlopen("https://www.wikidata.org/wiki/Special:EntityData/"+qtag+".json").read().decode("utf-8")
            entity = json.loads(contents)["entities"][qtag]
            tag = entity["labels"].get("en",{"value":qtag})["value"]
            tags[qtag] = tag

        for form in lexeme["forms"]:
            flist = []
            for qfeature in form["grammaticalFeatures"]:
                feature  = features.get(qfeature)
                if feature == None:
                    contents = urllib.request.urlopen("https://www.wikidata.org/wiki/Special:EntityData/"+qfeature+".json").read().decode("utf-8")
                    entity = json.loads(contents)["entities"][qfeature]
                    feature = entity["labels"].get("en",{"value":qfeature})["value"]
                    features[qfeature] = feature
                flist.append(feature)
            flists = lexicon.setdefault(lang,{}).setdefault(tag,[])
            if flist not in flists:
                flists.append(flist)

for lang,tags in lexicon.items():
    for tag,forms in tags.items():
        print(lang,tag,forms)
