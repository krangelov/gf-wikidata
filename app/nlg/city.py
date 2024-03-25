import pgf
from wordnet import *
from nlg.util import *
# from nlg.lists import *

def render(cnc, lexeme, entity):
	yield "<div class='infobox'><table border=1>"
	# show the flag and the coat of arms if available
	for media,qual in get_medias("P18",entity):
		yield "<tr><td><img src='"+escape(media)+"' width=250/></td><tr>"
		break
	# show the location
	for media,qual in get_medias("P242",entity):
		yield "<tr><td><img src='"+escape(media)+"' width=250></td></tr>"
		break
	yield "</table></div>"

	country_qids = get_items("P17", entity)
	if country_qids:
		cn = mkCN(mkCN(w.city_1_N),mkAdv(w.in_1_Prep,mkNP(cnc.get_lex_fun(country_qids[0][0]))))
	else:
		cn = mkCN(w.city_1_N)

	phr=mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme),mkNP(aSg_Det,cn)))),fullStopPunct)
	yield "<p>"+cnc.linearize(phr)+"</p>"


	# Adjust to city.py
	# State largest city in the country
	# [Tokyo] is the largest city in [Japan] with a population of [00000] inhabitants.
	#for city_qid, city_pop, country_qid in largest_cities:
	#	if entity["id"] == country_qid:
	#		city_name = cnc.get_lex_fun(city_qid)
	#		city_population = mkAdv(w.with_Prep,mkNP(mkDecimal(int(city_pop)),w.inhabitant_1_N))
	#		np = mkNP(mkDet(the_Quant,singularNum,mkOrd(w.large_1_A)),mkCN(w.city_1_N))
	#		if cnc.name in ["ParseFre", "ParseSpa"]:
	#			np = mkNP(np, mkAdv(w.of_1_Prep,mkNP(lexeme)))
	#		else:
	#			np = mkNP(np, mkAdv(w.in_1_Prep,mkNP(lexeme)))
	#		np = mkNP(np, city_population)
	#		phr = mkPhr(mkUtt(mkS(mkCl(mkNP(city_name),np))),fullStopPunct)
	#		yield " " + cnc.linearize(phr)