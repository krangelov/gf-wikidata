from os import name
import pgf
import wordnet as w
from wordnet.api import *
from nlg.util import *
from nlg.lists import *



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


	print(' ')
	yield "<h2>Demographics</h2>"

	# state life expectancy
	# [Country name] has the highest/lowest life expectancy in [continent / the world], with an average of [XX] years.
	# GOAL: [Norway] has the (second/third/...) highest/lowest life expectancy (in Europe / in the world), with an average of XX years.
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
			# The life expectancy is [XX] years.
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(the_Det, w.CompoundN(w.life_1_N,w.expectancy_1_N)), mkNP(mkDigits(int(life_expectancy)), w.year_1_N)))),fullStopPunct)
			yield " " + cnc.linearize(phr)

	
	# State largest city in the country
	# The largest city in Spain / The country's largest city... is Madrid with a population of...
	# [Tokyo] is the largest city in [Japan] with a population of [00000] inhabitants.
	for city_qid, city_pop, country_qid in largest_cities:
		if entity["id"] == country_qid:
			city_name = cnc.get_lex_fun(city_qid)
			#print('CITY_NAME: ', city_name)
			city = mkCN(mkCN(w.city_1_N), mkAdv(w.in_1_Prep,mkNP(lexeme)))
			city_population = mkAdv(w.with_Prep,mkNP(mkDigits(int(city_pop)),w.inhabitant_1_N))
			cn = mkCN(mkCN(mkAP(mkOrd(w.large_1_A)), city), city_population)
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(city_name),mkNP(theSg_Det,cn)))),fullStopPunct)
			yield cnc.linearize(phr)
	
	

	# State basic form of government
	basic_form = get_items("P122", entity, qual=False)
	if basic_form:
		for qid in form_of_government:
			if basic_form[0] == qid[0]:
				bfog = qid[1]
				#cn = qid[1]
				
	

	# Property: office held by HEAD OF STATE
	position_state = False
	office_state = get_items("P1906", entity)
	if office_state:
		for qid, quad in office_state: 
			if qid == 'Q844944':
				# no 'chairwoman' in WordNet
				position_state = mkCN(w.chairman_N, mkAdv(w.of_1_Prep, mkNP(the_Det, w.presidency_2_N))) # chairman of the presidency
				break
			entity_office = get_entity(qid)
			if "P279" in entity_office['claims']: # P270 = subclass of
				for subclass_qid, quad in get_items("P279", entity_office):
					if subclass_qid == 'Q15995642' or subclass_qid == 'Q611644': #religious leader / Catholic bishop
						position_state = mkCN(w.pope_1_N)
						break
					elif subclass_qid == 'Q30461' or subclass_qid == 'Q248577': #president / president of the republic
						position_state = "president"
						break
					elif subclass_qid == 'Q43292': #sultan
						position_state = mkCN(w.sultan_N)
						break
					elif subclass_qid == 'Q7645115': #supreme leader
						position_state = mkCN(w.supreme_2_A, w.leader_1_N)
						break
					elif subclass_qid == 'Q166382': #emir
						position_state = mkCN(w.emir_N)
						break
					elif subclass_qid == 'Q39018': #emperor
						position_state = mkCN(w.emperor_1_N)
						break
					elif subclass_qid == 'Q116' or subclass_qid == 'Q12097' or subclass_qid == 'Q16511993': #monarch / king / queen
						position_state = "monarch"
					
					#match subclass_qid:
					#	case 'Q15995642' | 'Q611644':
					#		position_state = w.pope_1_N
					#		break
					#	case 'Q30461' | 'Q248577':
					#		position_state = "president"
					#		break
	


	# Property: office held by HEAD OF GOVERNMENT
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
				position_gov = mkCN((w.CompoundN(w.state_1_N, w.counsellor_1_N)))
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
					elif subclass_qid == 'Q1670755':
						position_gov = mkCN((w.CompoundN(w.chief_1_N, w.minister_2_N)))
						break
					elif subclass_qid == 'Q14212' or subclass_qid == 'Q58869896' or subclass_qid == 'Q2632935': # prime minister / Head of Government of Liechtenstein / minister of state
						position_gov = mkCN(w.prime_1_A, w.minister_2_N)	
						break



	#print('POSITION_STATE: ', position_state)
	#print('POSITION_GOV: ', position_gov)


# Special condition if the head of state and the head of government is the same person as in Oman


	# State current head of state (HOS), previous HOS, HOS' gender and kinship:
	name_date_state = {}
	#name_date_state = []
	current_head_state = False
	father_name = False
	mother_name = False
	
	property_head_state = get_items("P35", entity)
	if property_head_state:
		for head_state, qual in property_head_state:
			head_entity = get_entity(head_state)
			name_head_state = cnc.get_person_name(head_entity)
			if 'P582' not in qual: # No end date == current head of state
				current_head_state = name_head_state

				# Checking gender
				gender = w.he_Pron if any(name_qid == "Q6581097" for name_qid, qual in get_items("P21", head_entity)) else w.she_Pron

				# Checking kinship
				if "P22" in head_entity['claims']: # Checking if there is a 'father' property (P22)
					for father_qid, quad in get_items("P22", head_entity):
						father_entity = get_entity(father_qid)
						father_name = cnc.get_person_name(father_entity)
				
				if "P25" in head_entity['claims']: # Checking if there is a 'mother' property (P25)
					for mother_qid, quad in get_items("P25", head_entity):
						mother_entity = get_entity(mother_qid)
						mother_name = cnc.get_person_name(mother_entity)
				
			if 'P582' in qual: # End date == previous heads of state
				#gender_prev = w.he_Pron if any(name_qid == "Q6581097" for name_qid, qual in get_items("P21", head_entity)) else w.she_Pron
				#print('GENDER_PREV: ', gender_prev)
				# Creating a dict {name : date}
				date = get_time_qualifier("P582",qual) # Checking end date
				name_date_state[name_head_state] = date
				#name_date_state.append((name_head_state, date, gender_prev))
				#print('name_date_state: ', name_date_state)


	# Sorting dict by dates 
	if name_date_state:
		sorted_dates_state = dict(sorted(name_date_state.items(), key=lambda x: x[1], reverse=True))
		#print('sorted_dates_state: ', sorted_dates_state)
		#sorted_dates_state = sorted(name_date_state, key=lambda x: x[1], reverse=True)
		prev_head_state = next(iter(sorted_dates_state.keys()))
		#gender_prev_head = sorted_dates_state[0][-1]
		#prev_head_state = sorted_dates_state[0][0]

	
	print(' ')
	yield "<h2>Politics</h2>"

	# Linearizing:
	# [Country name] is a [basic form of government], with [position] [name] as head of state. 
	# He/She succeeded [his/her father/mother] [position] [name] in the position. 
	# The current head of government is [position] [name]. 
	# He/She took office after [position] [name].
	# GOAL: The current head of government is Prime Minister Pedro Sanchez, *who* assumed/took office after Mariano Rajoy.
	# phr = mkPhr(mkUtt(mkS(mkCl(mkNP(the_Det,cn), mkNP(current_head_state), mkSC(mkQS(pastTense, mkQCl(w.whoSg_IP, mkVP(w.take_12_V2, mkNP(mkCN(w.office_4_N, mkAdv(w.after_Prep,mkNP(prev_head_state))))))))))),fullStopPunct)

	if basic_form:
		if current_head_state:
			if position_state == 'monarch':
				if gender == w.he_Pron:
					position_state = mkCN(w.king_1_N)
				elif gender == w.she_Pron:
					position_state = mkCN(w.queen_2_N)
			elif position_state == 'president':
				if gender == w.he_Pron:
					position_state = mkCN(w.presidentMasc_3_N)
				elif gender == w.she_Pron:
					position_state = mkCN(w.presidentFem_3_N)
			elif not position_state:
				# There is BFOG and HOS but not POSITION
				phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme), mkNP(aSg_Det, mkCN(bfog, mkAdv(w.with_Prep, mkNP(mkNP(current_head_state), mkAdv(w.as_Prep, mkNP(mkCN(w.head_4_N,mkAdv(w.of_1_Prep,mkNP(w.state_1_N)))))))))))), fullStopPunct)
				yield " "+cnc.linearize(phr)
			
			#FIRST SENTENCE
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme), mkNP(aSg_Det, mkCN(bfog, mkAdv(w.with_Prep, mkNP(mkCN(mkCN(position_state, mkNP(current_head_state)), mkAdv(w.as_Prep, mkNP(mkCN(w.head_4_N,mkAdv(w.of_1_Prep,mkNP(w.state_1_N))))))))))))), fullStopPunct)
			yield " "+cnc.linearize(phr)

			#SECOND SENTENCE
			if prev_head_state:
				if prev_head_state == father_name:
					if position_state == mkCN(w.king_1_N) or position_state == mkCN(w.queen_2_N):
						phr = mkPhr(mkUtt(mkS(pastTense, mkCl(mkNP(gender), mkVP(w.succeed_V2, mkNP(mkQuant (gender), mkCN(mkCN(w.father_1_N), mkNP(mkCN(mkCN(mkCN(w.king_1_N), mkNP(prev_head_state)), mkAdv(w.in_1_Prep, mkNP(the_Det, w.position_6_N)))))))))),fullStopPunct)
						yield " "+cnc.linearize(phr)
					else:
						phr = mkPhr(mkUtt(mkS(pastTense, mkCl(mkNP(gender), mkVP(w.succeed_V2, mkNP(mkQuant (gender), mkCN(mkCN(w.father_1_N), mkNP(mkCN(mkCN(position_state, mkNP(prev_head_state)), mkAdv(w.in_1_Prep, mkNP(the_Det, w.position_6_N)))))))))),fullStopPunct)
						yield " "+cnc.linearize(phr)
				elif prev_head_state == mother_name:
					if position_state == mkCN(w.king_1_N) or position_state == mkCN(w.queen_2_N):
						phr = mkPhr(mkUtt(mkS(pastTense, mkCl(mkNP(gender), mkVP(w.succeed_V2, mkNP(mkQuant (gender), mkCN(mkCN(w.mother_1_N), mkNP(mkCN(mkCN(mkCN(w.queen_2_N), mkNP(prev_head_state)), mkAdv(w.in_1_Prep, mkNP(the_Det, w.position_6_N)))))))))),fullStopPunct)
						yield " "+cnc.linearize(phr)
					else:
						phr = mkPhr(mkUtt(mkS(pastTense, mkCl(mkNP(gender), mkVP(w.succeed_V2, mkNP(mkQuant (gender), mkCN(mkCN(w.mother_1_N), mkNP(mkCN(mkCN(position_state, mkNP(prev_head_state)), mkAdv(w.in_1_Prep, mkNP(the_Det, w.position_6_N)))))))))),fullStopPunct)
						yield " "+cnc.linearize(phr)
				else:
					if position_state:
						phr = mkPhr(mkUtt(mkS(pastTense, mkCl(mkNP(gender), mkVP(w.succeed_V2, mkNP(mkCN(position_state, mkNP(mkNP(prev_head_state), mkAdv(w.in_1_Prep, mkNP(the_Det, w.position_6_N))))))))),fullStopPunct)
						yield " "+cnc.linearize(phr)
					else:
						phr = mkPhr(mkUtt(mkS(pastTense, mkCl(mkNP(gender), mkVP(w.succeed_V2, mkNP(mkNP(prev_head_state), mkAdv(w.in_1_Prep, mkNP(the_Det, w.position_6_N))))))),fullStopPunct)
						yield " "+cnc.linearize(phr)

		else:
			# If there is basic form of gov but not head of state:
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme), mkNP(aSg_Det, bfog)))), fullStopPunct)
			yield " " + cnc.linearize(phr)


	

	# State current head of government (HOG), previous HOG, HOG' gender and kinship:
	name_date_gov = {}
	current_head_gov = False
	property_head_gov = get_items("P6", entity)
	if property_head_gov:
		for head_government, qual in property_head_gov:
			head_entity = get_entity(head_government)
			name_head_gov = cnc.get_person_name(head_entity)
			if 'P582' not in qual: # No end date == current head of government
				current_head_gov = name_head_gov

				# Checking gender
				gender = w.he_Pron if any(name_qid == "Q6581097" for name_qid, qual in get_items("P21", head_entity)) else w.she_Pron

				# Checking kinship
				if "P22" in head_entity['claims']: # Checking if there is a 'father' property (P22)
					for father_qid, quad in get_items("P22", head_entity):
						father_entity = get_entity(father_qid)
						father_name = cnc.get_person_name(father_entity)
				
				if "P25" in head_entity['claims']: # Checking if there is a 'mother' property (P25)
					for mother_qid, quad in get_items("P25", head_entity):
						mother_entity = get_entity(mother_qid)
						mother_name = cnc.get_person_name(mother_entity)

			if 'P582' in qual: # End date == previous heads of government
				# Creating a dict {name : date}
				date = get_time_qualifier("P582",qual) # Checking end date
				name_date_gov[name_head_gov] = date

	# Sorting dict by dates
	if name_date_gov:
		sorted_dates_gov = dict(sorted(name_date_gov.items(), key=lambda x: x[1], reverse=True))
		prev_head_gov = next(iter(sorted_dates_gov.keys()))


	# Linearizing:
	# The current head of government is [position] [name].
	# He/She took office after [position] [name].
	if current_head_gov:
		if position_gov:
			if position_gov == 'president':
				if gender == w.he_Pron:
					position_gov = mkCN(w.presidentMasc_3_N)
				elif gender == w.she_Pron:
					position_gov = mkCN(w.presidentFem_3_N)

			# The current head of gov is [position] [name].
			cn = mkCN(w.current_A, mkCN(w.head_4_N,mkAdv(w.of_1_Prep,mkNP(w.government_1_N))))
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(the_Det,cn), mkNP(mkCN(position_gov, mkNP(current_head_gov)))))),fullStopPunct)
			yield " "+cnc.linearize(phr)

			if prev_head_gov:
				if prev_head_gov == father_name:
					# He/She took office after his/her father [position] [name].
					phr = mkPhr(mkUtt(mkS(pastTense, mkCl(mkNP(gender), mkVP(w.take_12_V2, mkNP(mkCN(w.office_4_N, mkAdv(w.after_Prep, mkNP(mkQuant(gender), mkCN(w.father_1_N, mkNP(mkCN(position_gov, mkNP(prev_head_gov)))))))))))),fullStopPunct)
					yield " "+cnc.linearize(phr)
				elif prev_head_gov == mother_name:
					# He/She took office after his/her mother [position] [name].
					phr = mkPhr(mkUtt(mkS(pastTense, mkCl(mkNP(gender), mkVP(w.take_12_V2, mkNP(mkCN(w.office_4_N, mkAdv(w.after_Prep, mkNP(mkQuant(gender), mkCN(w.mother_1_N, mkNP(mkCN(position_gov, mkNP(prev_head_gov)))))))))))),fullStopPunct)
					yield " "+cnc.linearize(phr)
				else:
					# [He/She] took office after [position] [name].
					phr = mkPhr(mkUtt(mkS(pastTense, mkCl(mkNP(gender), mkVP(w.take_12_V2, mkNP(mkCN(w.office_4_N, mkAdv(w.after_Prep, mkNP(mkCN(position_gov, mkNP(prev_head_gov)))))))))),fullStopPunct)
					yield " "+cnc.linearize(phr)

		else:
			# The current head of gov is [name].
			cn = mkCN(w.current_A, mkCN(w.head_4_N,mkAdv(w.of_1_Prep,mkNP(w.government_1_N))))
			phr = mkPhr(mkUtt(mkS(mkCl(mkNP(the_Det,cn), mkNP(current_head_gov)))),fullStopPunct)
			yield " "+cnc.linearize(phr)

			if prev_head_gov:
				if prev_head_gov == father_name:
					phr = mkPhr(mkUtt(mkS(pastTense, mkCl(mkNP(gender), mkVP(w.take_12_V2, mkNP(mkCN(w.office_4_N, mkAdv(w.after_Prep, mkNP(mkQuant(gender), mkCN(w.father_1_N, mkNP(prev_head_gov)))))))))),fullStopPunct)
					yield " "+cnc.linearize(phr)
				elif prev_head_gov == mother_name:
					phr = mkPhr(mkUtt(mkS(pastTense, mkCl(mkNP(gender), mkVP(w.take_12_V2, mkNP(mkCN(w.office_4_N, mkAdv(w.after_Prep, mkNP(mkQuant(gender), mkCN(w.mother_1_N, mkNP(prev_head_gov)))))))))),fullStopPunct)
					yield " "+cnc.linearize(phr)
				else:
					# [He/She] took office after [prev head of gov].
					phr = mkPhr(mkUtt(mkS(pastTense, mkCl(mkNP(gender), mkVP(w.take_12_V2, mkNP(mkCN(w.office_4_N, mkAdv(w.after_Prep, mkNP(prev_head_gov)))))))),fullStopPunct)
					yield " "+cnc.linearize(phr)
		
	
			
	


	


	yield "</p>"
