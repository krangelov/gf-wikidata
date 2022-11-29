import pgf
import wordnet as w
from wordnet.api import *
from nlg.util import *

def render(db, lexeme, cnc, entity):
    for value in entity["claims"]["P17"]:
        country_qid = value["mainsnak"]["datavalue"]["value"]["id"]
        break
		
    if country_qid:
        cn = w.PossNP(mkCN(w.capital_3_N),mkNP(pgf.ExprFun(get_lex_fun(db, country_qid))))
    else:
        cn = mkCN(w.capital_3_N)

    s=cnc.linearize(mkS(mkCl(mkNP(lexeme),mkNP(the_Det,cn))))
    yield "<p>"+escape(s)+"</p>"
