from daison import *
from wordnet.semantics import *
from html import escape
import hashlib

def get_lex_fun(db, qid):
    with db.run("w") as t:
        for synset_id in t.cursor(synsets_qid, qid):
            for lexeme_id in t.cursor(lexemes_synset, synset_id):
                for lexeme in t.cursor(lexemes, lexeme_id):
                    return lexeme.lex_fun
    return None

def get_items(prop,entity):
	items = []
	for value in entity["claims"].get(prop,[]):
		items.append((value["mainsnak"]["datavalue"]["value"]["id"],value.get("qualifiers",{})))
	return items

def get_quantities(prop,entity):
	quantities = []
	for value in entity["claims"].get(prop,[]):
		try:
			amount = float(value["mainsnak"]["datavalue"]["value"]["amount"])
		except:
			continue
		quantities.append((amount,value.get("qualifiers",{})))
	return quantities

def get_medias(prop,entity):
	medias = []
	for value in entity["claims"].get(prop,[]):
		try:
			img = value["mainsnak"]["datavalue"]["value"]
		except KeyError:
			continue
		img = img.replace(' ','_')
		h = hashlib.md5(img.encode("utf-8")).hexdigest()
		img = "https://upload.wikimedia.org/wikipedia/commons/"+h[0]+"/"+h[0:2]+"/"+img
		medias.append((img,value.get("qualifiers",{})))
	return medias

def get_time_qualifier(prop,quals):
	for value in quals.get(prop,[]):
		return value["datavalue"]["value"]["time"]
	return None

def capit(s):
	return s[0].upper()+s[1:]
