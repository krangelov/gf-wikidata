from os import name
import pgf
import wordnet as w
from wordnet.api import *
from nlg.util import *
from nlg.lists import *



def render(cnc, lexeme, entity):
	yield "<div class='infobox'><table border=1>"
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

	yield "</table></div>"


	# start the text generation
	yield "<p>"

	# it is a country
	class_qids = get_items("P31",entity,qual=False)
	if "Q112099" in class_qids:
		cn = mkCN(w.CompoundN(w.island_1_N,w.state_4_N))
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
		population = int(population_list[0][0])
		cn = mkCN(cn,mkAdv(w.with_Prep,mkNP(mkNum(population),w.inhabitant_1_N)))
	else:
		population = None
	phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme),mkNP(aSg_Det,cn)))),fullStopPunct)
	yield cnc.linearize(phr)
	
	# list neighbours
	neighbours = []
	for neighbour_qid,qual in get_items("P47",entity):
		neighbour_expr = cnc.get_lex_fun(neighbour_qid)
		if neighbour_expr != None and neighbour_expr != w.european_union_NP and "P582" not in qual:
			neighbour_expr = mkNP(neighbour_expr)
			direction_qid = get_item_qualifier("P654",qual)
			if direction_qid:
				direction = cnc.get_lex_fun(direction_qid)
				if direction:
					if cnc.name in ["ParseBul"]:
						neighbour_expr = mkNP(neighbour_expr,mkAdv(w.to_2_Prep,mkNP(aSg_Det,direction)))
					else:
						neighbour_expr = mkNP(neighbour_expr,mkAdv(w.to_2_Prep,mkNP(the_Det,direction)))
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
		elif cnc.name in ["ParseBul"]: #ProDrop
			if len(neighbours) > 1:
				phr = mkPhr(mkUtt(mkS(mkCl(mkNP(w.ProDrop(w.she_Pron)),mkVP(w.have_1_V2,mkNP(aPl_Det,mkCN(mkCN(w.border_1_N),mkAdv(w.with_Prep,mkNP(w.and_Conj,neighbours)))))))),fullStopPunct)
			else:
				phr = mkPhr(mkUtt(mkS(mkCl(mkNP(w.ProDrop(w.she_Pron)),mkVP(w.have_1_V2,mkNP(aSg_Det,mkCN(mkCN(w.border_1_N),mkAdv(w.with_Prep,neighbours[0]))))))),fullStopPunct)
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
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(theSg_Det,w.area_6_N), mkAdv(w.of_1_Prep, mkNP(mkDecimal(int(area)), sq_km))))),fullStopPunct)
		elif cnc.name in ["ParseSpa"]:
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(theSg_Det,w.area_6_N), w.UseComp_ser(w.CompAdv(mkAdv(w.of_1_Prep, mkNP(mkDecimal(int(area)), sq_km))))))),fullStopPunct)
		else:
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(theSg_Det,w.area_6_N),mkNP(mkDecimal(int(area)),sq_km)))),fullStopPunct)
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


	yield '<h2 class="gp-page-title">'+cnc.linearize(w.demographic_N)+'</h2>'

	# state life expectancy
	# [Country name] has the highest/lowest life expectancy in [continent / the world], with an average of [XX] years.
	# GOAL: [Norway] has the (second/third/...) highest/lowest life expectancy (in Europe / in the world), with an average of XX years.
	expectancy_list = sorted(((life_expectancy,get_time_qualifier("P585",quals)) for life_expectancy,quals in get_quantities("P2250",entity)),key=lambda p: p[1],reverse=True)
	if expectancy_list:
		life_expectancy = expectancy_list[0][0]

		for qid, expectancy, region in top:
			if life_expectancy == expectancy:
				# [Country name] has the highest life expectancy in [continent / the world], with an average of [XX] years.
				phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme), mkVP(w.have_1_V2, mkNP(theSg_Det, mkCN(mkCN(mkAP(mkOrd(w.high_1_A)), w.life_expectancy_N), 
				      mkAdv(w.in_1_Prep, (mkNP(region, mkAdv(w.with_Prep, mkNP(a_Det, mkCN(mkCN(w.average_1_N), mkAdv(w.of_1_Prep, mkNP(mkDecimal(int(life_expectancy)), w.year_1_N)))))))))))))), fullStopPunct)
				yield " " + cnc.linearize(phr)
				top_or_bottom = True
				break
		else:
			for qid, expectancy, region in bottom:
				if life_expectancy == expectancy:
					# [Country name] has the lowest life expectancy in [continent / the world], with an average of [XX] years.
					phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme), mkVP(w.have_1_V2, mkNP(theSg_Det, mkCN(mkCN(mkAP(mkOrd(w.low_1_A)), w.life_expectancy_N),
					      mkAdv(w.in_1_Prep, (mkNP(region, mkAdv(w.with_Prep, mkNP(a_Det, mkCN(mkCN(w.average_1_N), mkAdv(w.of_1_Prep, mkNP(mkDecimal(int(life_expectancy)), w.year_1_N)))))))))))))), fullStopPunct)
					yield " " + cnc.linearize(phr)
					break
			else:
				# The life expectancy is [XX] years.
				phr = mkPhr(mkUtt(mkS(mkCl(mkNP(the_Det, w.life_expectancy_N), mkNP(mkDecimal(int(life_expectancy)), w.year_1_N)))),fullStopPunct)
				yield " " + cnc.linearize(phr)

	fertility_list = sorted(((life_expectancy,get_time_qualifier("P585",quals) or "X") for life_expectancy,quals in get_quantities("P4841",entity)),key=lambda p: p[1],reverse=True)
	if fertility_list:
		fertility = float(fertility_list[0][0])
		yield " " + cnc.linearize(mkPhr(mkUtt(mkCl(mkNP(theSg_Det, w.fertility_1_N), mkNP(mkNum(fertility), mkCN(mkCN(w.child_2_N), mkAdv(w.per_Prep,mkNP(w.woman_1_N)))))), fullStopPunct))

	suicide_list = sorted(((life_expectancy,get_time_qualifier("P585",quals) or "X") for life_expectancy,quals in get_quantities("P3864",entity)),key=lambda p: p[1],reverse=True)
	if suicide_list:
		suicide = float(suicide_list[0][0])
#		yield " " + str(suicide)
	
	# State largest city in the country
	# [Tokyo] is the largest city in [Japan] with a population of [00000] inhabitants.
	for city_qid, city_pop, country_qid in largest_cities:
		if entity["id"] == country_qid:
			city_name = cnc.get_lex_fun(city_qid)
			city = mkCN(mkCN(w.city_1_N), mkAdv(w.in_1_Prep,mkNP(lexeme)))
			city_population = mkAdv(w.with_Prep,mkNP(mkDecimal(int(city_pop)),w.inhabitant_1_N))
			cn = mkCN(mkCN(mkAP(mkOrd(w.large_1_A)), city), city_population)
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(city_name),mkNP(theSg_Det,cn)))),fullStopPunct)
			yield " " + cnc.linearize(phr)

	hdi_list = sorted(((hdi,get_time_qualifier("P585",quals)) for hdi,quals in get_quantities("P1081",entity)),key=lambda p: p[1],reverse=True)
	if hdi_list:
		hdi = float(hdi_list[0][0])
		quality = mkCN(w.human_1_A, w.development_2_N)
		if hdi >= 0.800:
			quality = mkCN(mkAP(w.very_AdA,w.high_1_A), quality)
		elif hdi >= 0.700:
			quality = mkCN(mkAP(w.high_1_A), quality)
		elif hdi >= 0.550:
			quality = mkCN(mkAP(w.medium_1_A), quality)
		else:
			quality = mkCN(mkAP(w.low_1_A), quality)

		yield " " + cnc.linearize(mkPhr(mkUtt(mkCl(mkNP(theSg_Det,w.country_1_N), mkVP(w.have_1_V2, mkNP(aSg_Det, quality)))))) + " (HDI " + str(hdi) + ")."


# P2997 maturity
# P3000 mariage
# P2834 tax rate
# P2855 VAT

	# Stating the official religion
	religion = False
	property_religion = get_items("P3075", entity)
	if property_religion:
		for qid, quad in property_religion: 
			if qid == 'Q432': # Islam
				religion = mkCN(w.islam_2_N)
				break
			elif qid == 'Q5043': # Christianity
				religion = mkCN(w.christianity_1_N)
				break
			elif qid == 'Q9268': # Judaism
				religion = mkCN(w.judaism_2_N)
				break
			elif qid == 'Q748': # Buddhism
				religion = mkCN(w.buddhism_1_N)
				break
			elif qid == 'Q752470': # Finnish Orthodox Church --> Eastern Orthodox Christianity
				religion = mkCN(w.eastern_4_A, mkCN(w.orthodox_3_A, w.christianity_1_N))
				break
			elif qid == 'Q9592' or qid == 'Q1841': # Catholic Church / Catholicism
				religion = mkCN(w.catholicism_N)
				break
			# elif qid == 'Q163943': # Druze
			# 	religion = mkCN(druze) # not in Wikidata
			# 	break
			# elif qid == 'Q728697': # Laicism
			# 	religion = mkCN(laicism) # not in Wikidata
			# 	break
			# elif qid == 'Q1379849': # Evangelical Lutheran Church of Finland
			# 	religion = mkCN(lutheranism) #not in Wikidata
			# 	break
			
	if religion:
		# The official religion is [religion].
		# Future work: allowing multiple religions simultaneously.
		phr = mkPhr(mkUtt(mkS(mkCl(mkNP(the_Det, mkCN(w.official_3_A, w.religion_2_N)), mkNP(religion)))),fullStopPunct)
		yield " " + cnc.linearize(phr)
	
	yield '<h2 class="gp-page-title">'+cnc.linearize(w.education_1_N)+'</h2>'

	literacy_list = sorted(((literacy,get_time_qualifier("P585",quals)) for literacy,quals in get_quantities("P6897",entity)),key=lambda p: p[1],reverse=True)
	if literacy_list:
		literacy_rate = float(literacy_list[0][0])
		literacy_rate = mkNP(literacy_rate,w.percent_MU)
	else:
		literacy_rate = None

	min_age = False
	max_age = False
	obj = mkCN(w.age_1_N)
	min_age_list = sorted(((literacy,get_time_qualifier("P585",quals) or "X") for literacy,quals in get_quantities("P3270",entity)),key=lambda p: p[1],reverse=True)
	if min_age_list:
		min_age = int(min_age_list[0][0])
		obj = mkCN(obj,mkAdv(w.from_Prep,mkNP(mkNum(min_age),w.year_1_N)))
	max_age_list = sorted(((literacy,get_time_qualifier("P585",quals) or "X") for literacy,quals in get_quantities("P3271",entity)),key=lambda p: p[1],reverse=True)
	if max_age_list:
		max_age = int(max_age_list[0][0])
		obj = mkCN(obj,mkAdv(w.to_1_Prep,mkNP(mkNum(max_age),w.year_1_N)))
	if min_age or max_age:
		phr = mkPhr(mkUtt(mkCl(mkNP(w.education_1_N), w.AdvAP(mkAP(w.obligatory_1_A), mkAdv(w.for_Prep, mkNP(aPl_Det,w.PossNP(mkCN(w.child_1_N), mkNP(obj))))))), fullStopPunct)
		yield " "+cnc.linearize(phr)
		
		if literacy_rate:
			phr = mkPhr(mkUtt(mkCl(this_NP, mkVP(w.result_in_V2, mkNP(aSg_Det,mkCN(w.CompoundN(w.literacy_N,w.rate_4_N), mkAdv(w.of_1_Prep, literacy_rate)))))),fullStopPunct)
			yield " "+cnc.linearize(phr)
	else:
		if literacy_rate:
			phr = mkPhr(mkUtt(mkCl(mkNP(theSg_Det,w.CompoundN(w.literacy_N,w.rate_4_N)), literacy_rate)),fullStopPunct)
			yield " "+cnc.linearize(phr)

	out_of_school_list = sorted(((out_of_school,get_time_qualifier("P585",quals)) for out_of_school,quals in get_quantities("P2573",entity)),key=lambda p: p[1],reverse=True)
	if out_of_school_list:
		out_of_school = int(out_of_school_list[0][0])
		yield " "+cnc.linearize(mkPhr(mkUtt(mkCl(mkNP(mkNum(out_of_school), w.child_1_N), mkAdv(w.out_of_3_Prep,mkNP(theSg_Det, w.CompoundN(w.education_1_N,w.system_1_N))))),fullStopPunct))
		if population:
			phr = mkPhr(mkUtt(mkCl(this_NP, mkVP(w.amount_to_2_V2, mkNP(mkNP(round((out_of_school/population)*100,2), w.percent_MU), mkAdv(w.of_1_Prep, mkNP(theSg_Det, w.population_1_N)))))),fullStopPunct)
			yield " "+cnc.linearize(phr)

	divisions = cnc.get_lexemes("P150",entity,qual=False)
	if divisions:
		yield '<h2 class="gp-page-title">'+cnc.linearize(mkNP(aPl_Det,mkCN(w.administrative_A,w.unit_3_N)))+'</h2>'
		yield '<p>'+cnc.linearize(mkCl(mkNP(theSg_Det,w.country_1_N),mkVP(w.have_1_V2,mkNP(thePl_Det,mkCN(w.following_2_A,mkCN(w.administrative_A,w.unit_3_N))))))+':'
		if len(divisions) < 5:
			column_count = 1
		elif len(divisions) < 10:
			column_count = 2
		else:
			column_count = 4
		yield "<ul style='column-count: "+str(column_count)+"'>"
		for division in divisions:
			yield "<li>"+cnc.linearize(division)+"</li>"
		yield '</ul></p>'

	# State basic form of government
	bfog = None
	for basic_form in get_items("P122", entity, qual=False):
		for qid in form_of_government:
			if basic_form == qid[0]:
				bfog = qid[1]
				
	

	# Property: office held by HEAD OF STATE
	# Future work:
	# Presidency of Bosnia and Herzegovina (Q844944) --> The presidency is divided between three people, one Serb, one Croatian and one Bosnian president
	# French co-prince of Andorra (Q19808845) --> parliamentary coprincipality (check form of gov)
	# Episcopal Co-Prince (Q19808790) --> Andorra (two heads of state)
	# Member of the Swiss Federal Council (Q11811941) --> Switzerland: special case, the head of state is a federal council with 7 members
	# O le Ao o le Malo (Q1258128) --> Samoan for "head of state"
	position_state = False
	office_state = get_items("P1906", entity)
	if office_state:
		for qid, quad in office_state: 
			if qid == 'Q844944':
				# no 'chairwoman' in WordNet
				position_state = mkCN(w.chairman_N, mkAdv(w.of_1_Prep, mkNP(the_Det, w.presidency_2_N))) # Bosnia and Herzegovina
				break
			elif qid == 'Q955006': # United Arab Emirates
				position_state = "president"
				break
			elif qid == 'Q25711499': # State of Qatar
				position_state = mkCN(w.emir_N)
				break
			elif qid == 'Q63415597' or qid == 'Q2457774': # Lichtenstein / Monaco
				position_state = mkCN(w.prince_N)
				break
			elif qid == 'Q258045': # San Marino
				position_state = mkCN((w.CompoundN(w.captain_1_N, w.regent_1_N)))
				break
			elif qid == 'Q2081829': # Afghanistan
				position_state = mkCN(w.amir_N)
				break
			elif qid == 'Q1402561': # Burkina Faso
				position_state = mkCN(w.military_2_A, w.leader_1_N)
				break
			elif qid == 'Q1472951': # Jamaica
				position_state = mkCN(w.governor_general_N)
				break
			elif qid == 'Q102181806': # Libya
				position_state = mkCN(w.chairman_N, mkAdv(w.of_1_Prep, mkNP(the_Det, mkCN(w.presidential_1_A, w.council_1_N))))
				break
			elif qid == 'Q63107773': # Sudan
				position_state = mkCN(w.chairman_N, mkAdv(w.of_1_Prep, mkNP(the_Det, mkCN(w.transitional_A, mkCN(w.military_2_A, w.council_1_N)))))
				break
			
			entity_office = get_entity(qid)
			if "P279" in entity_office['claims']: # P270 = subclass of
				for subclass_qid, quad in get_items("P279", entity_office):
					if subclass_qid == 'Q15995642' or subclass_qid == 'Q611644': # religious leader / Catholic bishop
						position_state = mkCN(w.pope_1_N)
						break
					elif subclass_qid == 'Q30461' or subclass_qid == 'Q248577': # president / president of the republic
						position_state = "president"
						break
					elif subclass_qid == 'Q43292': # sultan
						position_state = mkCN(w.sultan_N)
						break
					elif subclass_qid == 'Q7645115': # supreme leader
						position_state = mkCN(w.supreme_2_A, w.leader_1_N)
						break
					elif subclass_qid == 'Q166382': # emir
						position_state = mkCN(w.emir_N)
						break
					elif subclass_qid == 'Q39018': # emperor
						position_state = mkCN(w.emperor_1_N)
						break
					elif subclass_qid == 'Q382844': # governor-general
						position_state = mkCN(w.governor_general_N)
						break
					elif subclass_qid == 'Q116' or subclass_qid == 'Q12097' or subclass_qid == 'Q16511993': #monarch / king / queen
						position_state = "monarch"
						break
					
					

	# Property: office held by HEAD OF GOVERNMENT
	# Future work: consider the possibility of multiple HOG as in Afghanistan OR even multiple positions (P1906) 
	# as in Jamaica or Antigua and Barbuda
	position_gov = False
	office_gov = get_items("P1313", entity)
	if office_gov:
		for qid, quad in office_gov: 
			if qid == 'Q2387238': # President of the Pontifical Commission for the Vatican City State
				position_gov = mkCN(w.presidentMasc_3_N, mkAdv(w.of_1_Prep, mkNP(the_Det, mkCN(w.pontifical_1_A, w.commission_1_N)))) 
				break
			elif qid == 'Q7240364' or qid == 'Q702650': # North Korea / Taiwan
				position_gov = mkCN(w.premier_2_N)
				break
			elif qid == 'Q191827': # Ireland
				position_gov = mkCN(w.taoiseach_N)
				break
			elif qid == 'Q258045': # San Marino
				position_gov = mkCN((w.CompoundN(w.captain_1_N, w.regent_1_N)))
				break
			elif qid == 'Q23747483' or qid == 'Q105234803': # Myanmar
				position_gov = mkCN((w.CompoundN(w.state_4_N, w.counsellor_1_N)))
				break
			elif qid == 'Q16020744': # Bosnia and Herzegovina
				# no 'chairwoman' in WordNet
				position_gov = mkCN(w.chairman_N, mkAdv(w.of_1_Prep, mkNP(the_Det, mkCN(w.council_1_N, mkAdv(w.of_1_Prep, mkNP(w.minister_2_N))))))
				break

			entity_office = get_entity(qid)
			if "P279" in entity_office['claims']: # P270 = subclass of
				for subclass_qid, quad in get_items("P279", entity_office):
					if subclass_qid == 'Q959664': # premier
						position_gov = mkCN(w.premier_2_N)	
						break
					elif subclass_qid == 'Q30461' or subclass_qid == 'Q248577': #president / president of the republic
						position_gov = "president"
						break
					elif subclass_qid == 'Q43292': # sultan
						position_gov = mkCN(w.sultan_N)
						break
					elif subclass_qid == 'Q484876': # chief executive officer
						position_gov = mkCN(mkCN(w.chief_1_N), mkNP(mkCN(w.executive_A, w.officer_2_N)))
						break
					elif subclass_qid == 'Q56022' or subclass_qid == 'Q373085': # Chancellor of Germany / chancellor
						position_gov = mkCN(w.chancellor_2_N)
						break
					elif subclass_qid == 'Q1670755': # chief minister
						position_gov = mkCN((w.CompoundN(w.chief_1_N, w.minister_2_N)))
						break
					elif subclass_qid == 'Q14212' or subclass_qid == 'Q58869896' or subclass_qid == 'Q2632935': # prime minister / Head of Government of Liechtenstein / minister of state
						position_gov = mkCN(w.prime_minister_2_N)
						break



# Future work: special condition if the head of state and the head of government is the same person as in Oman


	# State current head of state (HOS), previous HOS, HOS' gender and kinship:
	name_date_state = []
	curr_head_state_qid = None
	prev_head_state_qid = None
	for head_state, qual in get_items("P35", entity):
		if 'P582' not in qual: # No end date == current head of state
			curr_head_state_qid = head_state
		else: # End date == previous heads of state
			date = get_time_qualifier("P582",qual) # Checking end date
			name_date_state.append((head_state,date))

	# Sorting by dates 
	if name_date_state:
		name_date_state.sort(key=lambda x: x[1], reverse=True)
		prev_head_state_qid = name_date_state[0][0]

	# State current head of government (HOG), previous HOG, HOG' gender and kinship:
	name_date_gov = []
	curr_head_gov_qid = None
	prev_head_gov_qid = None
	for head_government, qual in get_items("P6", entity):
		if 'P582' not in qual: # No end date == current head of government
			curr_head_gov_qid = head_government
		else: # End date == previous heads of government
			date = get_time_qualifier("P582",qual) # Checking end date
			if date:
				name_date_gov.append((head_government,date))
			else:
				curr_head_gov_qid = head_government

	# Sorting by dates
	if name_date_gov:
		name_date_gov.sort(key=lambda x: x[1], reverse=True)
		prev_head_gov_qid = name_date_gov[0][0]

	entities = get_entity([curr_head_state_qid,prev_head_state_qid,curr_head_gov_qid,prev_head_gov_qid])

	yield '<h2 class="gp-page-title">'+cnc.linearize(w.politics_2_N)+'</h2>'

	# Linearizing:
	# [Country name] is a [basic form of government], with [position] [name] as head of state. 
	# He/She succeeded [his/her father/mother] [position] [name] in the position. 
	# FIRST SENTENCE
	if bfog:
		if curr_head_state_qid:
			head_entity = entities[curr_head_state_qid]
			curr_head_state = cnc.get_person_name(head_entity)

			# Checking gender
			gender = w.he_Pron if any(gender_qid == "Q6581097" for gender_qid, qual in get_items("P21", head_entity)) else w.she_Pron

			# Checking kinship
			father_qid = False
			mother_qid = False

			# Checking if there is a 'father' property (P22)
			for father_qid, quad in get_items("P22", head_entity):
				break

			# Checking if there is a 'mother' property (P25)
			for mother_qid, quad in get_items("P25", head_entity):
				break

			if position_state and curr_head_state:
				if position_state == 'monarch' and gender == w.he_Pron:
					position_state = mkCN(w.king_1_N)
				elif position_state == 'monarch' and gender == w.she_Pron:
					position_state = mkCN(w.queen_2_N)
				elif position_state == 'president' and gender == w.he_Pron:
					position_state = mkCN(w.presidentMasc_3_N)
				elif position_state == 'president' and gender == w.she_Pron:
					position_state = mkCN(w.presidentFem_3_N)
				# [position] [name]
				curr_head_state = mkNP(mkCN(position_state, curr_head_state))
				
			if curr_head_state:
				bfog = mkCN(bfog, mkAdv(w.with_Prep, mkNP(curr_head_state, mkAdv(w.as_Prep, mkNP(w.head_of_state_N)))))
			# [Country name] is a [basic form of government], with [curr_head_state] as head of state.
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme), mkNP(aSg_Det, bfog)))), fullStopPunct)
			yield " "+cnc.linearize(phr)

			# SECOND SENTENCE
			if prev_head_state_qid:
				head_entity = entities[prev_head_state_qid]
				prev_head_state = cnc.get_person_name(head_entity)

				if curr_head_state and prev_head_state:
					if prev_head_state_qid == father_qid:
						if position_state == mkCN(w.king_1_N) or position_state == mkCN(w.queen_2_N):
							# his/her father king [name]
							prev_head_state = mkNP(mkQuant(gender), mkCN(mkCN(w.father_1_N), mkNP(mkCN(mkCN(w.king_1_N), prev_head_state))))
						else:
							# his/her father [position] [name]
							prev_head_state = mkNP(mkQuant(gender), mkCN(mkCN(w.father_1_N), mkNP(mkCN(position_state, prev_head_state))))

					elif prev_head_state_qid == mother_qid:
						if position_state == mkCN(w.king_1_N) or position_state == mkCN(w.queen_2_N):
							# his/her mother queen [name]
							prev_head_state = mkNP(mkQuant(gender), mkCN(mkCN(w.mother_1_N), mkNP(mkCN(mkCN(w.queen_2_N), prev_head_state))))
						else:
							# his/her mother [position] [name]
							prev_head_state = mkNP(mkQuant(gender), mkCN(mkCN(w.mother_1_N), mkNP(mkCN(position_state), prev_head_state)))

					elif position_state:
						# [position] [name]
						prev_head_state = mkNP(mkCN(position_state, prev_head_state))

					# He/She succeeded [prev_head_state] in the position.
					phr = mkPhr(mkUtt(mkS(pastTense, mkCl(mkNP(gender), mkVP(mkVP(w.succeed_V2, prev_head_state), mkAdv(w.in_1_Prep, mkNP(the_Det, w.position_6_N)))))),fullStopPunct)
					yield " " + cnc.linearize(phr)
		
		else:
			# [Country name] is a [basic form of government]. 
			# There is BFOG but not HOS
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme), mkNP(aSg_Det, bfog)))), fullStopPunct)
			yield " " + cnc.linearize(phr)


	# Linearizing:
	# The current head of government is [position] [name], who took office after [position] [name].
	# GOAL: The current head of government is Prime Minister Pedro Sanchez, *who* assumed/took office after Mariano Rajoy.
	# ANOTHER EXAMPLE: The current head of gov who is Pedro took office after Mariano
	# cn = mkCN(w.current_A, mkCN(w.head_4_N,mkAdv(w.of_1_Prep,mkNP(w.government_1_N))))
	# test = mkPhr(mkUtt(mkNP(the_Det,mkCN(cn, mkRS(pastTense, mkRCl(which_RP(mkNP(curr_head_state)), mkVP(w.take_12_V2, mkNP(mkCN(w.office_4_N, mkAdv(w.after_Prep,mkNP(prev_head_state)))))))))),fullStopPunct)
	# We need to consider keeping the long sentence into two simple sentences for cases like the United Arab Emirates,
	# where there is no data for the previous head of government!
	if curr_head_gov_qid:
		head_entity = entities[curr_head_gov_qid]
		curr_head_gov = cnc.get_person_name(head_entity)

		if curr_head_gov:
			# Checking gender
			gender = w.he_Pron if any(gender_qid == "Q6581097" for gender_qid, qual in get_items("P21", head_entity)) else w.she_Pron

			# Checking kinship
			father_qid = False
			mother_qid = False

			# Checking if there is a 'father' property (P22)
			for father_qid, quad in get_items("P22", head_entity):
				break
			
			# Checking if there is a 'mother' property (P25)
			for mother_qid, quad in get_items("P25", head_entity):
				break

			subj = mkNP(the_Det,mkCN(w.current_A, w.PossNP(mkCN(w.head_4_N),mkNP(w.gen_Quant,mkCN(w.government_1_N)))))
			if position_gov:
				if position_gov == 'president':
					if gender == w.he_Pron:
						position_gov = mkCN(w.presidentMasc_3_N)
					elif gender == w.she_Pron:
						position_gov = mkCN(w.presidentFem_3_N)

				# [position] [name].
				curr_head_gov = mkNP(mkCN(position_gov, curr_head_gov))

			if prev_head_gov_qid:
				head_entity = entities[prev_head_gov_qid]
				prev_head_gov = cnc.get_person_name(head_entity)

				if prev_head_gov:
					if position_gov:
						prev_head_gov = mkNP(mkCN(position_gov, prev_head_gov))

					if prev_head_gov_qid == father_qid:
						# his/her father [name].
						prev_head_gov = mkNP(mkQuant(gender), mkCN(mkCN(w.father_1_N), prev_head_gov))
					elif prev_head_gov_qid == mother_qid:
						# He/She took office after his/her mother [name].
						prev_head_gov = mkNP(mkQuant(gender), mkCN(mkCN(w.mother_1_N), prev_head_gov))
					curr_head_gov = w.ExtRelNP(curr_head_gov, mkRS(pastTense, mkRCl(which_RP,mkVP(mkVP(w.take_12_V2, mkNP(w.office_4_N)), mkAdv(w.after_Prep, prev_head_gov)))))

			phr = mkPhr(mkUtt(mkS(mkCl(subj, curr_head_gov))),fullStopPunct)
			yield " "+cnc.linearize(phr)

	curr_organizations = set()
	prev_organizations = set()
	for org,qual in cnc.get_lexemes("P463",entity):
		if org != w.european_union_NP:
			org = mkNP(org)
		if "P582" not in qual:
			curr_organizations.add(org)
		else:
			prev_organizations.add(org)
	for org in curr_organizations:
		try:
			prev_organizations.remove(org)
		except KeyError:
			pass
	curr_organizations = mkNP(w.and_Conj, list(curr_organizations))
	if curr_organizations:
		phr = mkPhr(mkUtt(mkS(mkCl(mkNP(theSg_Det,w.country_1_N), mkNP(aSg_Det,w.PossNP(mkCN(w.member_4_N), curr_organizations))))),fullStopPunct)
		yield " "+cnc.linearize(phr)
	prev_organizations = mkNP(w.and_Conj, list(prev_organizations))
	if prev_organizations:
		phr = mkPhr(mkUtt(mkS(mkCl(mkNP(w.it_Pron), mkVP(w.also_AdV, mkVP(mkNP(aSg_Det,mkCN(w.former_3_A,w.PossNP(mkCN(w.member_4_N), prev_organizations)))))))),fullStopPunct)
		yield " "+cnc.linearize(phr)
	
	democracy_list = sorted(((democracy,get_time_qualifier("P585",quals)) for democracy,quals in get_quantities("P8328",entity)),key=lambda p: p[1],reverse=True)
	if democracy_list:
		democracy_index = float(democracy_list[0][0])
		adv = mkAdv(w.with_Prep, mkNP(mkNP(a_Quant,w.CompoundN(w.democracy_2_N,w.index_2_N)), mkAdv(w.of_1_Prep, mkNP(mkNum(democracy_index),w.point_10_N))))
		if democracy_index >= 9:
			quality = mkNP(a_Quant,mkCN(w.full_3_A,w.democracy_2_N))
		elif democracy_index >= 6:
			quality = mkNP(a_Quant,mkCN(w.democracy_2_N,mkAdv(w.with_Prep,mkNP(aPl_Det,w.flaw_3_N))))
		elif democracy_index >= 4:
			quality = mkNP(a_Quant,mkCN(w.hybrid_A,w.regime_1_N))
		else:
			quality = mkNP(a_Quant,mkCN(w.authoritarian_1_A,w.regime_1_N))
		phr = mkPhr(mkUtt(w.ExtAdvS(adv,mkS(mkCl(mkNP(lexeme), mkVP(passiveVP(mkVPSlash(w.rank_2_V2)),mkAdv(w.as_Prep,quality)))))), fullStopPunct)
		yield " "+cnc.linearize(phr)

	pol = positivePol
	for quality in get_items("P1552",entity,qual=False):
		if quality == "Q3174312":
			quality = mkNP(aSg_Det,mkCN(w.free_1_A,w.country_1_N))
			break
		elif quality == "Q47185282":
			quality = mkNP(aSg_Det,mkCN(w.free_1_A,w.country_1_N))
			pol     = negativePol
			break
		elif quality == "Q47185145":
			quality = mkNP(aSg_Det,mkCN(mkAP(w.partly_AdA,w.free_1_A),w.country_1_N))
			break
		elif quality == "Q7174":
			quality = mkNP(aSg_Det,mkCN(w.democratic_1_A,w.country_1_N))
			break
		quality = None
	phr = mkPhr(mkUtt(mkS(pol,mkCl(mkNP(mkNP(w.freedom_1_N), mkAdv(w.in_1_Prep, mkNP(theSg_Det,w.world_5_N))), mkVP(mkVPSlash(w.consider_6_V3,mkNP(w.it_Pron)), quality)))), fullStopPunct)
	yield " "+cnc.linearize(phr)

	agents = []
	for agent, qual in cnc.get_lexemes("P3461",entity):
		if "P582" not in qual:
			agents.append(mkNP(agent))
	agents = mkNP(w.and_Conj, agents)
	if agents:
		phr = mkPhr(mkUtt(mkS(positivePol,mkCl(mkNP(w.it_Pron),passiveVP(mkVPSlash(mkVPSlash(w.designate_4_V2),mkAdv(w.as_Prep,mkNP(aSg_Det,w.CompoundN(w.terrorist_N,w.state_4_N)))),agents)))), fullStopPunct)
		yield " "+cnc.linearize(phr)

	yield "</p>"

	economy = get_entities("P8744",entity,qual=False)
	if economy:
		economy = economy[0]
		yield '<h2 class="gp-page-title">'+cnc.linearize(w.economy_1_N)+'</h2>'

		yield "<p>"

		objs = []

		gdp_list = sorted(((gdp,get_time_qualifier("P585",quals)) for gdp,quals in get_quantities("P2131",economy)),key=lambda p: p[1],reverse=True)
		if gdp_list:
			gdp = int(gdp_list[0][0])
			objs.append(mkNP(gdp,w.dollar_MU))

		gdp_list = sorted(((gdp,get_time_qualifier("P585",quals)) for gdp,quals in get_quantities("P2132",economy)),key=lambda p: p[1],reverse=True)
		if gdp_list:
			gdpp = int(gdp_list[0][0])
			objs.append(mkNP(mkNP(gdpp,w.dollar_MU),w.per_capita_Adv))

		if objs:
			gdp = mkNP(w.and_Conj,objs)
			
			gdp_rate_list = sorted(((rate,get_time_qualifier("P585",quals)) for rate,quals in get_quantities("P2219",economy)),key=lambda p: p[1],reverse=True)
			if gdp_rate_list:
				gdp_rate = float(gdp_rate_list[0][0])
				if gdp_rate > 0:
					gdp = mkNP(gdp, mkAdv(w.with_Prep, mkNP(mkNP(aSg_Det,w.growth_3_N), mkAdv(w.of_1_Prep, mkNP(gdp_rate,w.percent_MU)))))
				elif gdp_rate < 0:
					gdp = mkNP(gdp, mkAdv(w.with_Prep, mkNP(mkNP(aSg_Det,w.decline_1_N), mkAdv(w.of_1_Prep, mkNP(-gdp_rate,w.percent_MU)))))
				else:
					pass

			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(theSg_Det, mkCN(w.gross_1_A, mkCN(w.domestic_1_A,w.product_2_N))), gdp))), fullStopPunct)
			yield " "+cnc.linearize(phr)

		inflation_list = sorted(((gdp,get_time_qualifier("P585",quals) or "X") for gdp,quals in get_quantities("P1279",economy)),key=lambda p: p[1],reverse=True)
		if inflation_list:
			inflation = float(inflation_list[0][0])
			yield " "+cnc.linearize(mkPhr(mkUtt(mkCl(mkNP(theSg_Det, w.CompoundN(w.inflation_1_N, w.rate_2_N)),mkNP(inflation,w.percent_MU))), fullStopPunct))

		reserve_list = sorted(((gdp,get_time_qualifier("P585",quals)) for gdp,quals in get_quantities("P2134",economy)),key=lambda p: p[1],reverse=True)
		if reserve_list:
			reserve = int(reserve_list[0][0])
			reserve = w.QuantityNP(mkDecimal(reserve),w.dollar_MU)
			phr = mkPhr(mkUtt(mkCl(mkNP(theSg_Det,w.country_2_N),mkVP(w.have_1_V2,mkNP(mkNP(aSg_Det, mkCN(w.total_1_A,w.reserve_2_N)), mkAdv(w.of_1_Prep, reserve))))), fullStopPunct)
			yield " "+cnc.linearize(phr)

		median_income = None
		median_income_list = sorted(((median_income,get_time_qualifier("P585",quals) or "X") for median_income,quals in get_quantities("P3529",entity)),key=lambda p: p[1],reverse=True)
		if median_income_list:
			median_income = int(median_income_list[0][0])
			median_income = mkNP(median_income,w.dollar_MU)

		gini = None
		gini_list = sorted(((gini,get_time_qualifier("P585",quals) or "X") for gini,quals in get_quantities("P1125",entity)),key=lambda p: p[1],reverse=True)
		if gini_list:
			gini = int(gini_list[0][0])
			conj = w.but_1_Conj
			if gini > 50:
				quality = mkCN(w.extreme_1_A, w.inequality_N)
			elif gini > 45:
				quality = mkCN(mkAP(w.very_AdA, w.high_1_A), w.inequality_N)
			elif gini > 40:
				quality = mkCN(w.high_1_A, w.inequality_N)
			elif gini > 35:
				quality = mkCN(w.moderate_1_A, w.inequality_N)
			elif gini > 30:
				quality = mkCN(w.moderate_1_A, w.equality_1_N)
				conj = w.and_Conj
			else:
				quality = mkCN(w.high_1_A, w.equality_1_N)
				conj = w.and_Conj
			gini = w.QuantityNP(mkDecimal(gini),w.percent_MU)

		if median_income and gini:
			phr = mkUtt(mkS(conj,mkS(mkCl(mkNP(theSg_Det, mkCN(w.median_3_A, w.income_N)), median_income)),
			                     mkS(mkCl(mkNP(mkDet(w.it_Pron), w.distribution_1_N), mkVP(w.show_2_V2, mkNP(aSg_Det,quality))))))
			yield " "+cnc.linearize(phr)+" ("+cnc.linearize(gini)+")."
		elif median_income:
			phr = mkPhr(mkUtt(mkCl(mkNP(theSg_Det, mkCN(w.median_3_A, w.income_N)), median_income)), fullStopPunct)
			yield " "+cnc.linearize(phr)
		elif gini:
			phr = mkUtt(mkCl(mkNP(theSg_Det, w.PossNP(mkCN(w.distribution_1_N), mkNP(w.income_N))), mkVP(w.show_2_V2, mkNP(aSg_Det,quality))))
			yield " "+cnc.linearize(phr)+" ("+cnc.linearize(gini)+")."

		for curr, qual in cnc.get_lexemes("P38",entity):
			if "P582" not in qual:
				phr = mkPhr(mkUtt(mkCl(mkNP(theSg_Det, mkCN(w.official_1_A, w.currency_1_N)), mkNP(theSg_Det, curr))), fullStopPunct)
				yield " "+cnc.linearize(phr)
				break

		unemployment_list = sorted(((gini,get_time_qualifier("P585",quals) or "X") for gini,quals in get_quantities("P1198",entity)),key=lambda p: p[1],reverse=True)
		if unemployment_list:
			unemployment = float(unemployment_list[0][0])
			phr = mkPhr(mkUtt(mkCl(mkNP(theSg_Det, w.unemployment_N), mkNP(unemployment, w.percent_MU))), fullStopPunct)
			yield " "+cnc.linearize(phr)
	yield "</p>"

	vats = []
	for vat,qual in get_quantities("P2855",entity):
		if "P582" not in qual:
			vat = mkNP(vat,w.percent_MU)
			products = []
			for lexeme in cnc.get_lexeme_qualifiers("P518", qual):
				products.append(mkNP(lexeme))
			products = mkNP(w.and_Conj, products)
			if products:
				vat = mkNP(vat,mkAdv(w.for_Prep,products))
			vats.append(vat)
	vats = mkNP(w.and_Conj, vats)

	ind_tax = []
	for tax,qual in get_quantities("P2834",entity):
		if "P582" not in qual:
			tax = mkNP(tax,w.percent_MU)
			value = get_quantity_qualifier("P2835",qual)
			if value:
				tax = mkNP(tax,mkAdv(w.above_Prep,mkNP(mkNum(value),w.krona_1_N)))
			ind_tax.append(tax)
	ind_tax = mkNP(w.and_Conj, ind_tax)

	if vats or ind_tax:
		yield "<p>"
		if vats:
			phr = mkPhr(mkUtt(mkCl(mkNP(theSg_Det,w.vat_1_N), vats)), fullStopPunct)
			yield " "+cnc.linearize(phr)
		if ind_tax:
			phr = mkPhr(mkUtt(mkCl(mkNP(theSg_Det,mkCN(w.individual_4_A,w.CompoundN(w.tax_N,w.rate_4_N))), ind_tax)), fullStopPunct)
			yield " "+cnc.linearize(phr)
		yield "</p>"
