import pgf
import wordnet as w
from wordnet.api import *
from nlg.util import *

def render(db, lexeme, cnc, entity):
	for value in entity["claims"]["P17"]:
		country_qid = value["mainsnak"]["datavalue"]["value"]["id"]
		break
		
	if country_qid:
		cn = mkCN(mkCN(w.city_1_N),mkAdv(w.in_1_Prep,mkNP(pgf.ExprFun(get_lex_fun(db, country_qid)))))
	else:
		cn = mkCN(w.city_1_N)

	s=cnc.linearize(mkS(mkCl(mkNP(lexeme),mkNP(aSg_Det,cn))))
	yield "<p>"+escape(s)+"</p>"
