import pgf
from daison import *
from wordnet.semantics import *
from html import escape
import hashlib

import pgf

class ConcrHelper:
	def __init__(self,cnc,db,lang,edit):
		self.cnc  = cnc
		self.db   = db
		self.edit = edit
		self.links = {}
		self.name  = cnc.name
		self.lang  = lang
		self.exprs = []

	def addLink(self,lexeme,qid):
		for lang,status in lexeme.status:
			if lang == self.cnc.name:
				break
		else:
			status = Status.Checked
		info = (qid,lexeme.lex_fun,status)
		self.links[lexeme.lex_fun] = info
		return info

	def removeLink(self,fun):
		del self.links[fun]

	def linearize(self,e,title=False):
		if self.edit:
			self.exprs.append(e)
		text = ""
		bind = True
		info = None
		def flatten(xs):
			nonlocal text, bind, info
			for x in xs:
				if isinstance(x,str):
					if title:
						x = x.title();
					if bind:
						bind = False
					else:
						text += " "
					if info:
						if self.edit:
							text += '<span class="'+info[2].name.lower()+'" lang="'+self.lang+'" onclick="edit_lex(this,event,\''+escape(info[1])+'\',\''+self.lang+'\')">'
						else:
							text += '<a href="index.wsgi?id='+info[0]+'&lang='+self.lang+'">'
						info = None
					text += escape(x)
				elif isinstance(x,pgf.Bracket):
					info = self.links.get(x.fun)
					if self.edit and info == None:
						self.links[x.fun] = False
						with self.db.run("r") as t:
							for lexeme_id in t.cursor(lexemes_fun, x.fun):
								for lexeme in t.cursor(lexemes, lexeme_id):
									info = self.addLink(lexeme, None)
					tmp  = info

					flatten(x.children)
					if tmp:
						if self.edit:
							text += '</span>'
						else:
							text += '</a>'
				elif isinstance(x,pgf.BIND):
					bind = True
		flatten(self.cnc.bracketedLinearize(e))
		return text[0].upper()+text[1:]

	lex_hacks = {
		"Q6452640": pgf.ExprFun("southeast_1_N"),
		"Q2381698": pgf.ExprFun("southwest_1_N"),
		"Q6497686": pgf.ExprFun("northeast_1_N"),
		"Q5491373": pgf.ExprFun("northwest_3_N"),
		"Q865":     pgf.ExprFun("taiwan_2_PN")
	}

	def get_lex_fun(self, qid, link=True):
		fun = self.lex_hacks.get(qid)
		if fun:
			return fun
		with self.db.run("r") as t:
			for synset_id in t.cursor(synsets_qid, qid):
				for lexeme_id in t.cursor(lexemes_synset, synset_id):
					for lexeme in t.cursor(lexemes, lexeme_id):
						if link:
							self.addLink(lexeme, qid)
						return pgf.ExprFun(lexeme.lex_fun)
		return None

	def get_lexemes(self,prop,entity,qual=True,link=True):
		items = []
		if qual:
			for value in entity["claims"].get(prop,[]):
				try:
					qid = value["mainsnak"]["datavalue"]["value"]["id"]
				except KeyError:
					continue
				fun = self.get_lex_fun(qid,link)
				if fun:
					items.append((fun,value.get("qualifiers",{})))
		else:
			for value in entity["claims"].get(prop,[]):
				try:
					qid = value["mainsnak"]["datavalue"]["value"]["id"]
				except KeyError:
					continue
				fun = self.get_lex_fun(qid,link)
				if fun:
					items.append(fun)
		return items

def get_items(prop,entity,qual=True):
	items = []
	if qual:
		for value in entity["claims"].get(prop,[]):
			try:
				items.append((value["mainsnak"]["datavalue"]["value"]["id"],value.get("qualifiers",{})))
			except KeyError:
				continue
	else:
		for value in entity["claims"].get(prop,[]):
			try:
				items.append(value["mainsnak"]["datavalue"]["value"]["id"])
			except KeyError:
				continue
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

def get_item_qualifier(prop,quals):
	for value in quals.get(prop,[]):
		try:
			return value["datavalue"]["value"]["id"]
		except KeyError:
			continue
	return None

def get_time_qualifier(prop,quals):
	for value in quals.get(prop,[]):
		try:
			return value["datavalue"]["value"]["time"]
		except KeyError:
			continue
	return None
