import pgf

import nlg.country
import nlg.capital
import nlg.city
from nlg.util import *

def render(db, lex_fun, cnc, entity): 
	class_qids = []
	for value in entity["claims"]["P31"]:
		class_qid = value["mainsnak"]["datavalue"]["value"]["id"]
		class_qids.append(class_qid)

	lex_expr = pgf.ExprFun(lex_fun)
	s=cnc.linearize(lex_expr).title()
	yield "<h1>"+escape(s)+"</h1>"
	
	if "Q6256" in class_qids:
		renderer = nlg.country.render
	elif "Q5119" in class_qids:
		renderer = nlg.capital.render
	elif "Q1549591" in class_qids:
		renderer = nlg.city.render
	elif "Q515" in class_qids:
		renderer = nlh.city.render
	else:
		renderer = None
		yield "<p>Define a renderer for at least one of the following classes: "+", ".join(class_qids)+"</p>"
		
	if renderer:
		for s in renderer(db,lex_expr,cnc,entity):
			yield s
