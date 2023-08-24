import pgf
from wordnet import *
from nlg.util import *

def render(cnc, lexeme, entity):
	yield "<div class='infobox'><table border=1>"
	for media,qual in get_medias("P18",entity):
		yield "<tr><td><img src='"+escape(media)+"' width=250/></td></tr>"
	yield "</table></div>"
	
	gender = get_items("P21",entity,qual=False)

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

	birthday = get_date("P569",entity)
	if birthday:
		description = mkCN(mkAP(mkVPSlash(mkVPSlash(w.bear_2_V2),birthday)),description)

	phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme),mkNP(aSg_Det,description)))),fullStopPunct)
	yield cnc.linearize(phr)

	if "Q6581072" in gender:
		pron = w.she_Pron
	else:
		pron = w.he_Pron

	advisors = []
	for advisor in get_entities(["P184"],entity,qual=False):
		name = cnc.get_person_name(advisor)
		if name:
			advisors.append(mkNP(name))
	if advisors:
		num = singularNum if len(advisors) == 1 else pluralNum
		advisors = mkNP(w.and_Conj,advisors)
		yield " "+cnc.linearize(mkPhr(mkUtt(mkS(pastTense,mkCl(mkNP(mkDet(pron,num),mkCN(w.doctoral_1_A, w.adviserMasc_N)),advisors))),fullStopPunct))

	teachers = []
	for teacher in get_entities(["P1066"],entity,qual=False):
		name = cnc.get_person_name(teacher)
		if name:
			teachers.append(mkNP(name))
	if teachers:
		num = singularNum if len(teachers) == 1 else pluralNum
		teachers = mkNP(w.and_Conj,teachers)
		yield " "+cnc.linearize(mkPhr(mkUtt(mkS(pastTense,mkCl(mkNP(pron),mkNP(aSg_Det,w.PossNP(mkCN(w.studentMasc_1_N),teachers))))),fullStopPunct))

	students = []
	for student in get_entities(["P802","P185"],entity,qual=False):
		name = cnc.get_person_name(student)
		if name:
			students.append(mkNP(name))
	if students:
		students = mkNP(w.and_Conj,students)	
		phr = mkPhr(mkUtt(mkS(pastTense,mkCl(mkNP(pron),mkNP(theSg_Det,w.PossNP(mkCN(w.supervisor_1_N),students))))),fullStopPunct)
		yield " "+cnc.linearize(phr)

