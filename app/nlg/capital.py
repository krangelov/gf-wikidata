import pgf
import wordnet as w
from wordnet.api import *
from nlg.util import *

def render(cnc, lexeme, entity):
	yield "<div class='infobox'><table border=1>"
	# show the flag and the coat of arms if available
	for media,qual in get_medias("P18",entity):
		yield "<tr><td><img src='"+escape(media)+"' width=250/></td></tr>"
		break
	# show the location
	for media,qual in get_medias("P242",entity):
		yield "<tr><td><img src='"+escape(media)+"' width=250></td></tr>"
		break
	yield "</table></div>"

	cn = mkCN(w.capital_3_N)
	for country_qid, qual in get_items("P17", entity):
		if "P582" not in qual:
			cn = w.PossNP(cn,mkNP(cnc.get_lex_fun(country_qid)))
			break

	s=mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme),mkNP(the_Det,cn)))),fullStopPunct)
	yield "<p>"+cnc.linearize(s)+"</p>"
