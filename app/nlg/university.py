from os import name
import pgf
from wordnet import *
from nlg.util import *
from nlg.lists import *


def render(cnc, lexeme, entity):
	# show the location
	yield "<div class='infobox'><table border=1>"
	for media,qual in get_medias("P18",entity):
		yield "<tr><td><img src='"+escape(media)+"' width=250></td></tr>"
		break
	yield "</table></div>"

	country = cnc.get_lexemes("P17",entity,qual=False)
	if country:
		yield cnc.linearize(mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme),mkNP(aSg_Det, mkCN(mkCN(w.university_1_N), mkAdv(country[0])))))),fullStopPunct))
