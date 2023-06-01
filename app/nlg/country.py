import pgf
import wordnet as w
from wordnet.api import *
from nlg.util import *

import json
import urllib.request

adjectives = [
     ("Q52062",  w.nordic_2_A),
     ("Q39731",  w.baltic_2_A),
     ("Q4412",   w.west_african_A),
     ("Q27433",  w.central_african_A),
     ("Q31945",  w.arabic_A),
     ("Q143487", w.arabic_A),
     ("Q779924", w.muslim_A)
    ]

regions = [
     "Q21195",      # Scandinavia
     "Q7204",	    # Middle East
     "Q27275",	    # Central Asia
     "Q27394",	    # Southern Africa
     "Q27407",	    # East Africa
     "Q27381",	    # North Africa
     "Q27509",      # Central Europe
     "Q27496",      # Western Europe
     "Q27468",      # Eastern Europe
     "Q27449",      # Southern Europe
     "Q18869",	    # Caucasus
     "Q35942",	    # Polynesia
     "Q37394",	    # Melanesia
     "Q3359409",	# Micronesia
     "Q664609"      # Caribbean
    ]


the_world = mkNP(theSg_Det, mkCN(w.world_1_N))
europe = mkNP(w.europe_1_PN)
asia = mkNP(w.asia_1_PN)
africa = mkNP(w.africa_PN)
north_america = mkNP(w.north_america_1_PN)
south_america = mkNP(w.south_america_1_PN)
insular_oceania = mkNP(w.insular_oceania_PN)

top = [
	("Q238", 85.41707, the_world),        # San Marino
	("Q17", 83.98488, the_world),         # Japan
	("Q16", 83.62, the_world),            # Canada
	("Q183", 80.8, the_world),            # Germany
	("Q39", 82.89756, the_world),         # Switzerland
	("Q238", 85.41707, europe),           # San Marino
	("Q183", 83.3, europe),               # Germany
	("Q39", 82.89756, europe),            # Switzerland
	("Q347", 82.6561, europe),            # Liechtenstein
	("Q38", 82.5439, europe),             # Italy
	("Q17", 83.98488, asia),              # Japan
	("Q334", 82.79512, asia),             # Singapore
	("Q801", 82.6, asia),                 # Israel
	("Q884", 82.02439, asia),             # South Korea
	("Q229", 80.508, asia),               # Cyprus
	("Q262", 76.078, africa),             # Algeria
	("Q1028", 75.821, africa),            # Morocco
	("Q948", 75.731, africa),             # Tunisia
	("Q1027", 74.39488, africa),          # Mauritius
	("Q1042", 74.30976, africa),          # Seychelles
	("Q16", 83.62, north_america),        # Canada
	("Q800", 79.831, north_america),      # Costa Rica
	("Q241", 79.742, north_america),      # Cuba
	("Q30", 78.69024, north_america),     # United States
	("Q804", 78.001, north_america),      # Panama
	("Q298", 80, south_america),          # Chile
	("Q77", 77.493, south_america),       # Uruguay
	("Q414", 76.577, south_america),      # Argentina
	("Q736", 76.327, south_america),      # Ecuador
	("Q155", 75.723, south_america),      # Brazil
	("Q408", 82.5, insular_oceania),      # Australia
	("Q664", 81.61244, insular_oceania),  # New Zealand
	("Q683", 75.013, insular_oceania),    # Samoa
	("Q252", 73.515, insular_oceania),    # Indonesia
	("Q678", 73.029, insular_oceania)     # Tonga
	]


bottom = [ # sorted from lower to higher life expectancy
	("Q1044", 51.835, the_world),         # Sierra Leone
	("Q929", 52.171, the_world),          # Central African Republic
	("Q657", 52.903, the_world),          # Chad
	("Q1033", 53.428, the_world),         # Nigeria
	("Q1008", 53.582, the_world),         # Ivory Coast
	("Q212", 71.47634, europe),           # Ukraine
	("Q159", 71.59293, europe),           # Russia
	("Q217", 71.61, europe),              # Moldova
	("Q227", 72.026, europe),             # Azerbaijan
	("Q232", 72.3, europe),               # Kazakhstan
	("Q889", 63.673, asia),               # Afghanistan
	("Q805", 64.953, asia),               # Yemen
	("Q819", 66, asia),                   # Laos
	("Q874", 67.835, asia),               # Turkmenistan
	("Q574", 68.881, asia),               # East Timor
	("Q1044", 51.835, africa),            # Sierra Leone
	("Q929", 52.171, africa),             # Central African Republic
	("Q657", 52.903, africa),             # Chad
	("Q1033", 53.428, africa),            # Nigeria
	("Q1008", 53.582, africa),            # Ivory Coast
	("Q790", 63.33, north_america),       # Haiti
	("Q242", 70.384, north_america),      # Belize
	("Q754", 70.673, north_america),      # Trinidad and Tobago
	("Q763", 71.33659, north_america),    # Saint Kitts and Nevis	
	("Q757", 73.179, north_america),      # Saint Vincent and the Grenadines
	("Q734", 66.65, south_america),       # Guyana
	("Q750", 69.125, south_america),      # Bolivia
	("Q730", 71.405, south_america),      # Suriname
	("Q733", 73.12, south_america),       # Paraguay
	("Q739", 74.381, south_america),      # Colombia
	("Q709", 65.23902, insular_oceania),  # Marshall Islands
	("Q691", 65.544, insular_oceania),    # Papua New Guinea
	("Q710", 68.46, insular_oceania),     # Kiribati
	("Q695", 69.12927, insular_oceania),  # Palau
	("Q702", 69.195, insular_oceania)     # Federated States of Micronesia
	]


#semipres_democracy = mkCN(semipresidential w.democracy_2_N)
#parl_coprincipality = mkCN(w.parliamentary_2_A, coprincipality)
#direct_system = mkCN(directorial w.system_4_N)

#peoples_republic = mkCN(people's w.republic_2_N) --> Q465613
#west_system = mkCN(w.westminster_PN, w.system_4_N)

republic = mkCN(w.republic_2_N)
monarchy = mkCN(w.monarchy_N)
autocracy = mkCN(w.autocracy_1_N)
oligarchy = mkCN(w.oligarchy_N)
federation = mkCN(w.federation_3_N)
dictatorchip = mkCN(w.dictatorship_N)
theocracy = mkCN(w.theocracy_2_N)
condominium = mkCN(w.condominium_2_N)
viceroyalty = mkCN(w.viceroyalty_N)
emirate = mkCN(w.emirate_1_N)
commonwealth = mkCN(w.commonwealth_4_N)
sharia = mkCN(w.shariah_1_N)
democracy = mkCN(w.democracy_2_N)
diarchy = mkCN(w.diarchy_N)
decentralization = mkCN(w.decentralization_2_N)
authoritarianism = mkCN(w.authoritarianism_N)
protectorate = mkCN(w.protectorate_N)
fam_dictatorship = mkCN(w.CompoundN(w.family_4_N, w.dictatorship_N))
crown_colony = mkCN(w.CompoundN(w.crown_1_N, w.colony_5_N))
part_democracy = mkCN(w.participatory_A, w.democracy_2_N)
islamic_state = mkCN(w.islamic_A, w.state_4_N)
dem_centralism = mkCN(w.democratic_1_A, w.centralism_N)
dem_republic = mkCN(w.democratic_1_A, w.republic_2_N)
com_dictatorship = mkCN(w.communist_A, w.dictatorship_N)
const_republic = mkCN(w.constitutional_2_A, w.republic_2_N)
islamic_republic = mkCN(w.islamic_A, w.republic_2_N)
unitary_state = mkCN(w.unitary_3_A, w.state_4_N)
const_monarchy = mkCN(w.constitutional_2_A, w.monarchy_N)
federal_republic = mkCN(w.federal_4_A, w.republic_2_N)
rep_democracy = mkCN(w.representative_3_A, w.democracy_2_N)
parl_system = mkCN(w.parliamentary_2_A, w.system_4_N)
soviet_republic = mkCN(w.soviet_A, w.republic_2_N)
asym_federalism = mkCN(w.asymmetric_A, w.federalism_N)
parl_republic = mkCN(w.parliamentary_2_A, w.republic_2_N)
pres_system = mkCN(w.presidential_1_A, w.system_4_N)
parl_monarchy = mkCN(w.parliamentary_2_A, w.monarchy_N)
abs_monarchy = mkCN(w.absolute_3_A, w.monarchy_N)
dual_monarchy = mkCN(w.dual_1_A, w.monarchy_N)
elect_monarchy = mkCN(w.elective_1_A, w.monarchy_N)
hered_monarchy = mkCN(w.hereditary_2_A, w.monarchy_N)
aristo_republic = mkCN(w.aristocratic_1_A, w.republic_2_N)
comp_monarchy = mkCN(w.composite_1_A, w.monarchy_N)
military_junta = mkCN(w.military_2_A, w.junta_N)
federal_monarchy = mkCN(w.federal_4_A, w.monarchy_N)
feudal_monarchy = mkCN(w.feudal_A, w.monarchy_N)
direct_democracy = mkCN(w.direct_2_A, w.democracy_2_N)
trans_government = mkCN(w.transitional_A, w.government_1_N)
parl_democracy = mkCN(w.parliamentary_2_A, w.democracy_2_N)
atm = mkCN(w.absolute_3_A, mkCN(w.theocratic_A, w.monarchy_N))
fed_parl_republic = mkCN(w.federal_4_A, mkCN(w.parliamentary_2_A, w.republic_2_N))


form_of_government = [
	("Q7270", republic),               # republic
	("Q7269", monarchy),               # monarchy
	("Q173424", autocracy),            # autocracy
	("Q79751" , oligarchy),            # oligarchy
	("Q43702" , federation),           # federation
	("Q317" , dictatorchip),           # dictatorchip
	("Q44405" , theocracy),            # theocracy
	("Q734818" , condominium),         # condominium
	("Q12356456" , viceroyalty),       # viceroyalty
	("Q189898" , emirate),             # emirate
	("Q2578692", commonwealth),        # commonwealth
	("Q482752", sharia),               # sharia
	("Q7174", democracy),              # democracy
	("Q936648", diarchy),              # diarchy
	("Q188961", decentralization),     # decentralization
	("Q6229", authoritarianism),       # authoritarianism
	("Q164142", protectorate),         # protectorate
	("Q5433328", fam_dictatorship),    # family dictatorship
	("Q1351282", crown_colony),        # crown colony
	("Q310988", part_democracy),       # participatory democracy
	("Q4204060", islamic_state),       # Islamic state
	("Q193852", dem_centralism),       # democratic centralism
	("Q5255892", dem_republic),        # democratic republic
	("Q117405807", com_dictatorship),  # communist dictatorship
	("Q1520223", const_republic),      # constitutional republic
	("Q672729", islamic_republic),     # Islamic Republic
	("Q41614", const_monarchy),        # constitutional monarchy
	("Q512187", federal_republic),     # federal republic
	("Q188759", rep_democracy),        # representative democracy
	("Q166747", parl_system),          # parliamentary system
	("Q1075404", soviet_republic),     # soviet republic 
	("Q179164", unitary_state),        # unitary state
	("Q3091398", asym_federalism),     # asymmetric federalism
	("Q4198907", parl_republic),       # parliamentary republic
	("Q49892", pres_system),           # presidential system
	("Q3330103", parl_monarchy),       # parliamentary monarchy
	("Q184558", abs_monarchy),         # absolute monarchy
	("Q2994894", dual_monarchy),       # dual monarchy
	("Q584683", elect_monarchy),       # elective monarchy
	("Q849242", hered_monarchy),       # hereditary monarchy
	("Q666680", aristo_republic),      # aristocratic republic
	("Q5156764", comp_monarchy),       # composite monarchy
	("Q25424534", military_junta),     # military junta
	("Q3208952", federal_monarchy),    # federal monarchy
	("Q4482688", feudal_monarchy),     # feudal monarchy
	("Q171174", direct_democracy),     # direct democracy
	("Q59281", trans_government),      # transitional government
	("Q3043547", parl_democracy),      # parliamentary democracy
	("Q4055127", atm),                 # absolute theocratic monarchy
	("Q5440547", fed_parl_republic)    # federal parliamentary republic
	]


def render(cnc, lexeme, entity):
	yield "<table class='infobox' border=1>"
	# show the flag and the coat of arms if available
	yield "<tr><td><table><tr>"
	has_flag = False
	for media,qual in get_medias("P41",entity):
		yield "<td><img src='"+escape(media)+"' height=78/></td>"
		has_flag = True
		break
	has_arms = False
	for media,qual in get_medias("P94",entity):
		yield "<td><img src='"+escape(media)+"' height=78/></td>"
		has_arms = True
		break
	yield "</tr><tr>"
	if has_flag:
		yield "<td>"+cnc.linearize(w.flag_1_N)+"</td>"
	else:
		yield "<td></td>"
	if has_arms:
		yield "<td>"+cnc.linearize(w.coat_of_arms_N)+"</td>"
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
	class_qids = get_items("P31",entity,qual=False)
	if "Q112099" in class_qids:
		cn = mkCN(w.CompoundN(w.island_1_N,w.state_3_N))
	else:
		cn = mkCN(w.country_2_N)

	# state the location in different ways
	part_of_qids  = get_items("P361",entity,qual=False)
	location_qids = get_items("P706",entity,qual=False)
	has_adjective = False
	for qid,adj in adjectives: # nordic, baltic, etc
		if qid in part_of_qids or qid in location_qids:
			cn = mkCN(adj,cn)
			has_adjective = True
			break

	region_nps  = []
	region_advs = []
	if "Q23522" in location_qids:  # on the balkans instead of in the balkans
		region_advs.append(mkAdv(w.on_1_Prep,mkNP(w.balkans_2_PN)))
	if not region_advs or entity["id"] == "Q43":
		for qid in regions: # the Caribbean, Melanesia, etc.
			if qid in part_of_qids or qid in location_qids:
				lex_fun = cnc.get_lex_fun(qid)
				if lex_fun:
					region_nps.append(mkNP(lex_fun))
	if region_nps:
		region_advs.append(mkAdv(w.in_1_Prep,mkNP(w.and_Conj,region_nps)))
	if region_advs:
		cn = mkCN(cn,mkAdv(w.and_Conj,region_advs))
	if not has_adjective and not region_advs:
		# add the continent if stated
		continent_lexemes = cnc.get_lexemes("P30",entity,qual=False)
		if continent_lexemes:
			cn = mkCN(cn,mkAdv(w.in_1_Prep,mkNP(continent_lexemes[0])))

	# add the number of inhabitants
	population_list = sorted(((population,get_time_qualifier("P585",quals)) for population,quals in get_quantities("P1082",entity)),key=lambda p: p[1],reverse=True)
	if population_list:
		population = population_list[0][0]
		cn = mkCN(cn,mkAdv(w.with_Prep,mkNP(mkDigits(int(population)),w.inhabitant_1_N)))
	phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme),mkNP(aSg_Det,cn)))),fullStopPunct)
	yield cnc.linearize(phr)
	
	# list neighbours
	neighbours = []
	for neighbour_qid,qual in get_items("P47",entity):
		neighbour_expr = cnc.get_lex_fun(neighbour_qid)
		if neighbour_expr != None and "P582" not in qual:
			neighbour_expr = mkNP(neighbour_expr)
			direction_qid = get_item_qualifier("P654",qual)
			if direction_qid:
				direction = cnc.get_lex_fun(direction_qid)
				if direction:
					neighbour_expr = mkNP(neighbour_expr,mkAdv(w.to_1_Prep,mkNP(the_Det,direction)))
			neighbours.append(neighbour_expr)
	if neighbours:
		if cnc.name in ["ParseSpa"]: #ProDrop
			if len(neighbours) > 1:
				phr = mkPhr(mkUtt(mkS(mkCl(mkNP(w.ProDrop(w.it_Pron)),mkVP(w.have_1_V2,mkNP(aPl_Det,mkCN(mkCN(w.border_1_N),mkAdv(w.with_Prep,mkNP(w.and_Conj,neighbours)))))))),fullStopPunct)
			else:
				phr = mkPhr(mkUtt(mkS(mkCl(mkNP(w.ProDrop(w.it_Pron)),mkVP(w.have_1_V2,mkNP(aSg_Det,mkCN(mkCN(w.border_1_N),mkAdv(w.with_Prep,neighbours[0]))))))),fullStopPunct)
		elif cnc.name in ["ParseFre"]: #"le pays" instead of 3perSg "il"
			if len(neighbours) > 1:
				phr = mkPhr(mkUtt(mkS(mkCl(mkNP(theSg_Det,w.country_2_N),mkVP(w.have_1_V2,mkNP(aPl_Det,mkCN(mkCN(w.border_1_N),mkAdv(w.with_Prep,mkNP(w.and_Conj,neighbours)))))))),fullStopPunct)
			else:
				phr = mkPhr(mkUtt(mkS(mkCl(mkNP(theSg_Det,w.country_2_N),mkVP(w.have_1_V2,mkNP(aSg_Det,mkCN(mkCN(w.border_1_N),mkAdv(w.with_Prep,neighbours[0]))))))),fullStopPunct)
		else:
			if len(neighbours) > 1:
				phr = mkPhr(mkUtt(mkS(mkCl(mkNP(w.it_Pron),mkVP(w.have_1_V2,mkNP(aPl_Det,mkCN(mkCN(w.border_1_N),mkAdv(w.with_Prep,mkNP(w.and_Conj,neighbours)))))))),fullStopPunct)
			else:
				phr = mkPhr(mkUtt(mkS(mkCl(mkNP(w.it_Pron),mkVP(w.have_1_V2,mkNP(aSg_Det,mkCN(mkCN(w.border_1_N),mkAdv(w.with_Prep,neighbours[0]))))))),fullStopPunct)
		yield " "+cnc.linearize(phr)

	# state the area
	area_list = sorted(((area,get_time_qualifier("P585",quals)) for area,quals in get_quantities("P2046",entity)),key=lambda p: p[1] or "",reverse=True)
	if area_list:
		area = area_list[0][0]
		if cnc.name in ["ParseSwe", "ParseGer", "ParseFin", "ParseDut"]:
			sq_km = w.CompoundN(w.square_1_N,w.kilometre_1_N)
		else:
			sq_km = mkCN(w.square_1_A,w.kilometre_1_N)
		if cnc.name in ["ParseFre"]:
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(theSg_Det,w.area_6_N), mkAdv(w.of_1_Prep, mkNP(mkDigits(int(area)), sq_km))))),fullStopPunct)
		elif cnc.name in ["ParseSpa"]:
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(theSg_Det,w.area_6_N), w.UseComp_ser(w.CompAdv(mkAdv(w.of_1_Prep, mkNP(mkDigits(int(area)), sq_km))))))),fullStopPunct)
		else:
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(theSg_Det,w.area_6_N),mkNP(mkDigits(int(area)),sq_km)))),fullStopPunct)
		yield " "+cnc.linearize(phr)

    # state the capital
	for capital, qual in cnc.get_lexemes("P36",entity):
		if "P582" not in qual:
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(the_Det,w.capital_3_N),mkNP(capital)))),fullStopPunct)
			yield " "+cnc.linearize(phr)
			break

    # state the official and other languages
	official_lang_qids = get_items("P37",entity,qual=False)
	official_langs = []
	for qid in official_lang_qids:
		lang = cnc.get_lex_fun(qid)
		if lang != None:
			official_langs.append(mkNP(lang))
	other_langs = []
	for qid in get_items("P2936",entity,qual=False):
		if qid not in official_lang_qids:
			lang = cnc.get_lex_fun(qid)
			if lang != None:
				if lang.name[-1] == "N":
					other_langs.append(mkNP(lang))
	if official_langs:
		if len(official_langs) > 1:
			my_det = thePl_Det			
		else:
			my_det = theSg_Det
		official_langs = mkNP(w.and_Conj,official_langs)
		other_langs = mkNP(w.and_Conj,other_langs)
		if other_langs:
			phr = mkPhr(mkUtt(mkS(w.but_1_Conj,mkS(mkCl(official_langs,mkNP(my_det,mkCN(w.official_1_A,mkCN(w.language_1_N))))),mkS(mkCl(other_langs,w.AdVVP(w.also_AdV,w.PassVPSlash(mkVPSlash(w.speak_3_V2))))))),fullStopPunct)
		else:
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(my_det,mkCN(w.official_1_A,mkCN(w.language_1_N))),official_langs))),fullStopPunct)
		yield " "+cnc.linearize(phr)
	elif other_langs:
		if len(other_langs) > 1:
			my_det = thePl_Det
		else:
			my_det = theSg_Det
		phr = mkPhr(mkUtt(mkS(mkCl(mkNP(my_det,mkCN(w.spoken_A,mkCN(w.language_1_N))),mkNP(w.and_Conj,other_langs)))),fullStopPunct)
		yield " "+cnc.linearize(phr)


	
	yield "<h2>Demographics</h2>"

	# state life expectancy
	# [Norway] has the (second/third/...) highest/lowest life expectancy (in Europe / in the world), with an average of XX years.
	expectancy_list = sorted(((life_expectancy,get_time_qualifier("P585",quals)) for life_expectancy,quals in get_quantities("P2250",entity)),key=lambda p: p[1],reverse=True)
	if expectancy_list:
		life_expectancy = expectancy_list[0][0]
		top_or_bottom = False

		for qid, expectancy, region in top:
			if life_expectancy == expectancy:
				phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme), mkVP(w.have_1_V2, mkNP(theSg_Det, mkCN(mkCN(mkAP(mkOrd(w.high_1_A)), (w.CompoundN(w.life_1_N, w.expectancy_1_N))), 
				      mkAdv(w.in_1_Prep, (mkNP(region, mkAdv(w.with_Prep, mkNP(a_Det, mkCN(mkCN(w.average_1_N), mkAdv(w.of_1_Prep, mkNP(mkDigits(int(life_expectancy)), w.year_1_N)))))))))))))), fullStopPunct)
				yield " " + cnc.linearize(phr)
				top_or_bottom = True
				break

		if not top_or_bottom:
			for qid, expectancy, region in bottom:
				if life_expectancy == expectancy:
					phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme), mkVP(w.have_1_V2, mkNP(theSg_Det, mkCN(mkCN(mkAP(mkOrd(w.low_1_A)), (w.CompoundN(w.life_1_N, w.expectancy_1_N))), 
					      mkAdv(w.in_1_Prep, (mkNP(region, mkAdv(w.with_Prep, mkNP(a_Det, mkCN(mkCN(w.average_1_N), mkAdv(w.of_1_Prep, mkNP(mkDigits(int(life_expectancy)), w.year_1_N)))))))))))))), fullStopPunct)
					yield " " + cnc.linearize(phr)
					top_or_bottom = True
					break

		if not top_or_bottom:
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(the_Det, w.CompoundN(w.life_1_N,w.expectancy_1_N)), mkNP(mkDigits(int(life_expectancy)), w.year_1_N)))),fullStopPunct)
			yield " " + cnc.linearize(phr)

	

	yield "<h2>Politics</h2>"

	# state basic form of government
	basic_form = get_items("P122", entity, qual=False)
	if basic_form:
		for qid in form_of_government:
			if basic_form[0] == qid[0]:
				cn = qid[1]
				phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme), mkNP(aSg_Det, cn)))), fullStopPunct)
				yield " " + cnc.linearize(phr)



	# The largest city in Spain / The country's largest city... is Madrid with a population of...


	monarchs = [("Q3847454", "mospain"),
	 			("Q1268572", "mosweden")]

	# Head of state (since ...) - succedded his father [...]
	# Spain is a [parliamentary monarchy] with [King Felipe VI] as head of state. 
	for head_state, qual in get_items("P35", entity):
		if 'P582' not in qual and any(qid == qual['P39'][0]['datavalue']['value']['id'] for qid, _ in monarchs):
			print("IT'S WORKING")
			

	qid_2 = 'Q191045'
	u2_2 = urllib.request.urlopen('https://www.wikidata.org/wiki/Special:EntityData/'+qid_2+'.json')
	result_2 = json.loads(u2_2.read())
	entity_2 = result_2["entities"][qid_2]

	for name_qid,qual in get_items("P735",entity_2):
		print('NAME_QID: ', name_qid)
		give_name = cnc.get_lex_fun(name_qid)
		print(give_name)

	
	#Head of government - predecessor [...]
	for head_gov_qid,qual in get_items("P6",entity):
		if 'P582' not in qual: # end date
			replaced_qid = get_item_qualifier("P1365",qual)
			#print('replaced_qid: ', replaced_qid)
			
	




	yield "</p>"
