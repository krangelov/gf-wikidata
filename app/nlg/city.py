import pgf
import wordnet as w
from wordnet.api import *
from nlg.util import *

def render(cnc, lexeme, entity):
	yield "<table class='infobox' border=1>"
	# show the flag and the coat of arms if available
	for media,qual in get_medias("P18",entity):
		yield "<tr><td><img src='"+escape(media)+"' width=250/></td><tr>"
		break
	# show the location
	for media,qual in get_medias("P242",entity):
		yield "<tr><td><img src='"+escape(media)+"' width=250></td></tr>"
		break
	yield "</table>"

	country_qids = get_items("P17", entity)
	if country_qids:
		cn = mkCN(mkCN(w.city_1_N),mkAdv(w.in_1_Prep,mkNP(cnc.get_lex_fun(country_qids[0][0]))))
	else:
		cn = mkCN(w.city_1_N)

	phr=mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme),mkNP(aSg_Det,cn)))),fullStopPunct)
	yield "<p>"+cnc.linearize(phr)+"</p>"
