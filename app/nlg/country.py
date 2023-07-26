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
		population = population_list[0][0]
		cn = mkCN(cn,mkAdv(w.with_Prep,mkNP(mkNum(int(population)),w.inhabitant_1_N)))
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


	yield '<h2 class="gp-page-title">'+cnc.linearize(w.demographic_N)+'</h2>'

	# state life expectancy
	# [Country name] has the highest/lowest life expectancy in [continent / the world], with an average of [XX] years.
	# GOAL: [Norway] has the (second/third/...) highest/lowest life expectancy (in Europe / in the world), with an average of XX years.
	expectancy_list = sorted(((life_expectancy,get_time_qualifier("P585",quals)) for life_expectancy,quals in get_quantities("P2250",entity)),key=lambda p: p[1],reverse=True)
	if expectancy_list:
		life_expectancy = expectancy_list[0][0]
		top_or_bottom = False

		for qid, expectancy, region in top:
			if life_expectancy == expectancy:
				# [Country name] has the highest life expectancy in [continent / the world], with an average of [XX] years.
				phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme), mkVP(w.have_1_V2, mkNP(theSg_Det, mkCN(mkCN(mkAP(mkOrd(w.high_1_A)), (w.CompoundN(w.life_1_N, w.expectancy_1_N))), 
				      mkAdv(w.in_1_Prep, (mkNP(region, mkAdv(w.with_Prep, mkNP(a_Det, mkCN(mkCN(w.average_1_N), mkAdv(w.of_1_Prep, mkNP(mkDigits(int(life_expectancy)), w.year_1_N)))))))))))))), fullStopPunct)
				yield " " + cnc.linearize(phr)
				top_or_bottom = True
				break

		if not top_or_bottom:
			for qid, expectancy, region in bottom:
				if life_expectancy == expectancy:
					# [Country name] has the lowest life expectancy in [continent / the world], with an average of [XX] years.
					phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme), mkVP(w.have_1_V2, mkNP(theSg_Det, mkCN(mkCN(mkAP(mkOrd(w.low_1_A)), (w.CompoundN(w.life_1_N, w.expectancy_1_N))), 
					      mkAdv(w.in_1_Prep, (mkNP(region, mkAdv(w.with_Prep, mkNP(a_Det, mkCN(mkCN(w.average_1_N), mkAdv(w.of_1_Prep, mkNP(mkDigits(int(life_expectancy)), w.year_1_N)))))))))))))), fullStopPunct)
					yield " " + cnc.linearize(phr)
					top_or_bottom = True
					break

		if not top_or_bottom:
			# The life expectancy is [XX] years.
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(the_Det, w.CompoundN(w.life_1_N,w.expectancy_1_N)), mkNP(mkDigits(int(life_expectancy)), w.year_1_N)))),fullStopPunct)
			yield " " + cnc.linearize(phr)

	
	# State largest city in the country
	# [Tokyo] is the largest city in [Japan] with a population of [00000] inhabitants.
	for city_qid, city_pop, country_qid in largest_cities:
		if entity["id"] == country_qid:
			city_name = cnc.get_lex_fun(city_qid)
			city = mkCN(mkCN(w.city_1_N), mkAdv(w.in_1_Prep,mkNP(lexeme)))
			city_population = mkAdv(w.with_Prep,mkNP(mkDigits(int(city_pop)),w.inhabitant_1_N))
			cn = mkCN(mkCN(mkAP(mkOrd(w.large_1_A)), city), city_population)
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(city_name),mkNP(theSg_Det,cn)))),fullStopPunct)
			yield " " + cnc.linearize(phr)
	

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
			name_date_gov.append((head_government,date))

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

	organizations = []
	for org in cnc.get_lexemes("P463",entity,qual=False):
		if org != w.european_union_NP:
			org = mkNP(org)
		organizations.append(org)
	organizations = mkNP(w.and_Conj, organizations)
	if organizations:
		phr = mkPhr(mkUtt(mkS(mkCl(mkNP(theSg_Det,w.country_1_N), mkNP(aSg_Det,w.PossNP(mkCN(w.member_4_N), organizations))))),fullStopPunct)
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
		phr = mkPhr(mkUtt(mkS(pol,mkCl(mkNP(w.it_Pron),passiveVP(mkVPSlash(mkVPSlash(w.designate_4_V2),mkAdv(w.as_Prep,mkNP(aSg_Det,w.terrorist_N))),agents)))), fullStopPunct)
		yield " "+cnc.linearize(phr)

	yield "</p>"

	yield '<h2 class="gp-page-title">'+cnc.linearize(w.economy_1_N)+'</h2>'
