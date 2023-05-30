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
	if not occupations:
		gender = get_items("P21",entity,qual=False)
		if get_items("P184",entity):
			occupations = mkCN(w.scientist_N)
		elif "Q6581097" in gender:
			occupations = mkCN(w.man_1_N)
		elif "Q6581072" in gender:
			occupations = mkCN(w.woman_1_N)
		else:
			occupations = mkCN(w.human_N)

	all_adjs,ds = cnc.get_demonyms("P27", entity)
	if ds:
		if all_adjs:
			ap = mkAP(w.and_Conj,[mkAP(adj) for adj in ds])
			description = mkCN(ap,occupations)
		else:
			np = mkNP(w.and_Conj,[mkNP(pn) for pn in ds])
			description = mkCN(occupations,mkAdv(w.from_Prep,np))
	else:
		description = occupations

	birthday = get_date("P569",entity)
	if birthday:
		description = mkCN(mkAP(mkVPSlash(mkVPSlash(w.bear_2_V2),birthday)),description)
	print(description)

	phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme),mkNP(aSg_Det,description)))),fullStopPunct)
	yield cnc.linearize(phr)
