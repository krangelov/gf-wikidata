import pgf
from wordnet import *
from nlg.util import *

def render(cnc, lexeme, entity):
	yield "<div class='infobox'><table border=1>"
	for media,qual in get_medias("P18",entity):
		yield "<tr><td><img src='"+escape(media)+"' width=250/></td></tr>"
	yield "</table></div>"
	
	gender = get_items("P21",entity,qual=False)

	yield "<p>"
	occupations = mkCN(w.and_Conj,[mkCN(occupation) for occupation in cnc.get_lexemes("P106", entity, qual=False)])
	if not occupations:
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

	birthday   = get_date("P569",entity)
	birthplace = cnc.get_lexemes("P19", entity, qual=False)
	if birthday or birthplace:
		verb = mkVPSlash(w.bear_2_V2)
		if birthday:
			verb = mkVPSlash(verb,birthday)
		if birthplace:
			verb = mkVPSlash(verb,mkAdv(birthplace[0]))
		description = mkCN(mkAP(verb),description)

	phr = mkPhr(mkUtt(mkS(mkCl(lexeme,mkNP(aSg_Det,description)))),fullStopPunct)
	yield cnc.linearize(phr)

	if "Q6581072" in gender:
		pron = w.she_Pron
	else:
		pron = w.he_Pron

	if cnc.name in ["ParseBul"]:
		useTense = presentTense
	else:
		useTense = pastTense

	advisors = []
	for advisor in get_entities(["P184"],entity,qual=False):
		name = cnc.get_person_name(advisor)
		if name:
			advisors.append(name)
	if advisors:
		num = singularNum if len(advisors) == 1 else pluralNum
		advisors = mkNP(w.and_Conj,advisors)
		yield " "+cnc.linearize(mkPhr(mkUtt(mkS(useTense,mkCl(mkNP(mkDet(pron,num),mkCN(w.doctoral_adviser_N)),advisors))),fullStopPunct))

	teachers = []
	for teacher in get_entities(["P1066"],entity,qual=False):
		name = cnc.get_person_name(teacher)
		if name:
			teachers.append(name)
	if teachers:
		num = singularNum if len(teachers) == 1 else pluralNum
		teachers = mkNP(w.and_Conj,teachers)
		yield " "+cnc.linearize(mkPhr(mkUtt(mkS(useTense,mkCl(mkNP(pron),mkNP(aSg_Det,w.PossNP(mkCN(w.studentMasc_1_N),teachers))))),fullStopPunct))

	students = []
	for student in get_entities(["P802","P185"],entity,qual=False):
		name = cnc.get_person_name(student)
		if name:
			students.append(name)
	if students:
		students = mkNP(w.and_Conj,students)	
		phr = mkPhr(mkUtt(mkS(useTense,mkCl(mkNP(pron),mkNP(theSg_Det,w.PossNP(mkCN(w.supervisor_1_N),students))))),fullStopPunct)
		yield " "+cnc.linearize(phr)
		
	yield "</p>"

	yield '<h2 class="gp-page-title">'+cnc.linearize(mkCN(w.personal_1_A,w.life_3_N))+'</h2>'
	yield "<p>"

	sisters  = []
	brothers = []
	for sibling in get_entities("P3373",entity,qual=False):
		name = cnc.get_person_name(sibling)
		if "Q6581072" in get_items("P21",sibling,qual=False):
			sisters.append(name)
		else:
			brothers.append(name)
	siblings = []
	if brothers:
		if len(brothers) == 1:
			det = aSg_Det
		else:
			det = mkDet(a_Quant,mkNum(len(brothers)))
		siblings.append(mkNP(det,mkCN(w.brother_1_N, mkNP(w.and_Conj,brothers))))
	if sisters:
		if len(sisters) == 1:
			det = aSg_Det
		else:
			det = mkDet(a_Quant,mkNum(len(sisters)))
		siblings.append(mkNP(det,mkCN(w.sister_1_N, mkNP(w.and_Conj,sisters))))
	siblings = mkNP(w.and_Conj, siblings)

	father = None
	for father in get_entities("P22",entity,qual=False):
		father = cnc.get_person_name(father)
		break
	mother = None
	for mother in get_entities("P25",entity,qual=False):
		mother = cnc.get_person_name(mother)
		break
	if mother and father:
		vp = mkVP(passiveVP(w.bear_2_V2), mkAdv(w.in_1_Prep, mkNP(theSg_Det,w.PossNP(mkCN(w.family_1_N),mkNP(w.and_Conj,[father,mother])))))
		if siblings:
			vp = w.ConjVPS(w.and_Conj,w.BaseVPS(w.MkVPS(mkTemp(useTense,simultaneousAnt),positivePol,vp), w.MkVPS(mkTemp(presentTense,simultaneousAnt),positivePol,mkVP(w.have_1_V2,siblings))))
			phr = mkPhr(mkUtt(w.PredVPS(mkNP(pron),vp)),fullStopPunct)
		else:
			phr = mkPhr(mkUtt(mkS(useTense,mkCl(mkNP(pron),vp))),fullStopPunct)
		yield " "+cnc.linearize(phr)
	elif mother:
		stmt = mkS(useTense,mkCl(mkNP(mkDet(pron,singularNum),mkCN(w.mother_1_N)),mother))
		if siblings:
			stmt = mkS(w.and_Conj, stmt, mkS(mkCl(mkNP(pron), mkVP(w.have_1_V2,siblings))))
		phr = mkPhr(mkUtt(stmt),fullStopPunct)
		yield " "+cnc.linearize(phr)
	elif father:
		stmt = mkS(useTense,mkCl(mkNP(mkDet(pron,singularNum),mkCN(w.father_1_N)),father))
		if siblings:
			stmt = mkS(w.and_Conj, stmt, mkS(mkCl(mkNP(pron), mkVP(w.have_1_V2,siblings))))
		phr = mkPhr(mkUtt(stmt),fullStopPunct)
		yield " "+cnc.linearize(phr)
	elif siblings:
		phr = mkPhr(mkUtt(mkS(mkCl(mkNP(pron), mkVP(w.have_1_V2,siblings)))),fullStopPunct)
		yield " "+cnc.linearize(phr)

	if has_novalue("P26",entity):
		phr = mkPhr(mkUtt(mkS(useTense, mkCl(mkNP(pron), mkVP(w.never_1_AdV,mkVP(w.marry_in_V))))),fullStopPunct)
		yield " "+cnc.linearize(phr)
	else:
		spouses = sorted([(spouse,
						   get_time_qualifier("P580",quals),
						   cnc.get_lexeme_qualifiers("P2842",quals),
						   get_time_qualifier("P582",quals),
						   get_item_qualifier("P1534",quals)) for spouse,quals in get_entities("P26",entity)],key=lambda p: p[1])
		for spouse,start,place,end,end_cause in spouses:
			name = cnc.get_person_name(spouse)
			vp = mkVP(w.marry_1_V2,name)
			if place:
				vp = mkVP(vp,mkAdv(place[0]))
			stmt = mkS(useTense, mkCl(mkNP(pron), vp))
			if start:
				stmt = w.ExtAdvS(str2date(start),stmt)
			phr = mkPhr(mkUtt(stmt),fullStopPunct)
			yield " "+cnc.linearize(phr)

			if end and end_cause != "Q4":
				if "Q6581072" in get_items("P21",spouse,qual=False):
					spouse_pron = w.she_Pron
				else:
					spouse_pron = w.he_Pron
				vp = mkVP(mkVP(w.divorce_2_V2,mkNP(spouse_pron)),str2date(end))
				phr = mkPhr(mkUtt(mkS(useTense, mkCl(mkNP(pron), vp))),fullStopPunct)
				yield " "+cnc.linearize(phr)

	deathday   = get_date("P570",entity)
	deathplace = cnc.get_lexemes("P20", entity, qual=False)
	if deathday or deathplace:
		deathmanner= get_items("P1196", entity, qual=False)
		killer = get_entities("P157", entity, qual=False)
		if killer:
			vp = passiveVP(w.kill_1_V2,cnc.get_person_name(killer[0]))
		elif "Q149086" in deathmanner:
			vp = passiveVP(w.kill_1_V2)
		else:
			vp = mkVP(w.die_1_V)
		if deathday:
			vp = mkVP(vp,deathday)
		if deathplace:
			vp = mkVP(vp,mkAdv(deathplace[0]))
		phr = mkPhr(mkUtt(mkS(useTense, mkCl(mkNP(pron), vp))),fullStopPunct)
		yield " "+cnc.linearize(phr)

	yield "</p>"

