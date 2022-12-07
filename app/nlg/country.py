import pgf
import wordnet as w
from wordnet.api import *
from nlg.util import *

def render(db, lexeme, cnc, entity):
	yield "<table class='infobox' border=1>"
	# show the flag and the coat of arms if available
	yield "<tr><td><table style='border-collapse: collapse'><tr>"
	has_flag = False
	for media,qual in get_medias("P41",entity):
		yield "<td><img src='"+escape(media)+"' width=125 height=78/></td>"
		has_flag = True
		break
	has_arms = False
	for media,qual in get_medias("P94",entity):
		yield "<td><img src='"+escape(media)+"' width=125 height=78/></td>"
		has_arms = True
		break
	yield "</tr><tr>"
	if has_flag:
		yield "<td style='text-align: center'>"+escape(capit(cnc.linearize(w.flag_1_N)))+"</td>"
	else:
		yield "<td></td>"
	if has_arms:
		yield "<td style='text-align: center'>"+escape(capit(cnc.linearize(w.blazon_N)))+"</td>"
	else:
		yield "<td></td>"
	yield "</tr></table></td></tr>"

	# show the location
	for media,qual in get_medias("P242",entity):
		yield "<tr><td><img src='"+escape(media)+"' width=250></td></tr>"
		break

	yield "</table>"


	# start the text generation
	yield "<p>"

	# it is a country
	class_qids = map(lambda x: x[0], get_items("P31",entity))
	if "Q112099" in class_qids:
		cn = mkCN(w.CompoundN(w.island_1_N,w.country_1_N))
	else:
		cn = mkCN(w.country_1_N)

	# state the location in different ways
	part_of_qids  = list(map(lambda x: x[0], get_items("P361",entity)))
	location_qids = list(map(lambda x: x[0], get_items("P706",entity)))
	if "Q52062" in part_of_qids:  # nordic
		cn = mkCN(w.nordic_2_A,cn)
		if "Q21195" in location_qids:
			cn = mkCN(cn,mkAdv(w.in_1_Prep,mkNP(w.scandinavia_2_PN)))
	elif "Q39731" in part_of_qids:  # baltic
		cn = mkCN(w.baltic_2_A,cn)
	elif "Q664609" in part_of_qids:
		cn = mkCN(cn,mkAdv(w.in_1_Prep,mkNP(w.caribbean_PN))) # caribbean
	elif "Q23522" in location_qids:
		cn = mkCN(cn,mkAdv(w.on_1_Prep,mkNP(w.balkans_2_PN))) # balkan
	else:
		# add the continent if stated
		continent_qids  = get_items("P30",entity)
		if continent_qids:
			cn = mkCN(cn,mkAdv(w.in_1_Prep,mkNP(pgf.ExprFun(get_lex_fun(db, continent_qids[0][0])))))

	# add the number of inhabitants
	population_list = sorted(((population,get_time_qualifier("P585",quals)) for population,quals in get_quantities("P1082",entity)),key=lambda p: p[1],reverse=True)
	if population_list:
		population = population_list[0][0]
		cn = mkCN(cn,mkAdv(w.with_Prep,mkNP(mkDigits(int(population)),w.inhabitant_1_N)))

	phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme),mkNP(aSg_Det,cn)))),fullStopPunct)
	yield escape(cnc.linearize(phr))

	# state the area
	area_list = sorted(((area,get_time_qualifier("P585",quals)) for area,quals in get_quantities("P2046",entity)),key=lambda p: p[1] or "",reverse=True)
	if area_list:
		area = area_list[0][0]
		if cnc.name in ["ParseSwe", "ParseGer"]:
			sq_km = w.CompoundN(w.square_1_N,w.kilometre_1_N)
		else:
			sq_km = mkCN(w.square_1_A,w.kilometre_1_N)
		phr = mkPhr(mkUtt(mkS(mkCl(mkNP(theSg_Det,w.area_6_N),mkNP(mkDigits(int(area)),sq_km)))),fullStopPunct)
		yield " "+escape(capit(cnc.linearize(phr)))

    # state the capital
	capital_qids  = get_items("P36",entity)
	if capital_qids:
		phr = mkPhr(mkUtt(mkS(mkCl(mkNP(the_Det,w.capital_3_N),mkNP(pgf.ExprFun(get_lex_fun(db, capital_qids[0][0])))))),fullStopPunct)
		yield " "+escape(capit(cnc.linearize(phr)))

	yield "</p>"
