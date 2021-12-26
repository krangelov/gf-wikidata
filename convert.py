import bz2
import json

lexicon = {}

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

        tag = lexeme["lexicalCategory"]

        sense_list = []
        for sense in lexeme["senses"]:
            sense_count = 0
            claims = sense.get("claims")
            if claims != None and claims != []:
                for snak in claims.get("P5137",[]):
                    mainsnak = snak["mainsnak"]
                    if "datavalue" in mainsnak:
                        q_sense = mainsnak["datavalue"]["value"]["id"]
                        sense_count = sense_count + 1

                        _,lemmas = lexicon.setdefault(q_sense,(tag,{}))
                        for lang,val in lexeme["lemmas"].items():
                            lemmas[lang] = val["value"]

            if sense_count == 0:
                l_sense = sense["id"]
                _,lemmas = lexicon.setdefault(l_sense,(tag,{}))
                for lang,val in lexeme["lemmas"].items():
                    lemmas[lang] = val["value"]

for sense,(tag,lemmas) in lexicon.items():
    print(sense,tag,lemmas)
