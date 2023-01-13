import pgf
import wordnet as w
from wordnet.api import *
from nlg.util import *

def render(cnc, lexeme, entity):
	yield "<table class='infobox' border=1>"
	for media,qual in get_medias("P18",entity):
		yield "<tr><td><img src='"+escape(media)+"' width=250/></td></tr>"
	yield "</table>"

	occupations = mkCN(w.and_Conj,[mkCN(occupation) for occupation in cnc.get_lexemes("P106", entity, qual=False)])
	if occupations:
		phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme),mkNP(aSg_Det,occupations)))),fullStopPunct)
		yield cnc.linearize(phr)
	else:
		phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme),mkNP(aSg_Det,w.human_N)))),fullStopPunct)
		yield cnc.linearize(phr)
