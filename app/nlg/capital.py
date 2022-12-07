import pgf
import wordnet as w
from wordnet.api import *
from nlg.util import *

def render(db, lexeme, cnc, entity):
    yield "<table class='infobox' border=1>"
    # show the flag and the coat of arms if available
    for media,qual in get_medias("P18",entity):
        yield "<tr><td><img src='"+escape(media)+"' width=250/></td></tr>"
        break
	# show the location
    for media,qual in get_medias("P242",entity):
        yield "<tr><td><img src='"+escape(media)+"' width=250></td></tr>"
        break
    yield "</table>"

    country_qids = get_items("P17", entity)
    if country_qids:
        cn = w.PossNP(mkCN(w.capital_3_N),mkNP(pgf.ExprFun(get_lex_fun(db, country_qids[0][0]))))
    else:
        cn = mkCN(w.capital_3_N)

    s=mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme),mkNP(the_Det,cn)))),fullStopPunct)
    yield "<p>"+escape(cnc.linearize(s))+"</p>"
