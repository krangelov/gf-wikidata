import pgf
import wordnet as w
from wordnet.api import *
from nlg.util import *

def render(cnc, lexeme, entity):
	yield "<table class='infobox' border=1>"
	for media,qual in get_medias("P18",entity):
		yield "<tr><td><img src='"+escape(media)+"' width=250/></td></tr>"
	yield "</table>"

	superclasses = mkCN(w.and_Conj,[mkCN(superclass) for superclass in cnc.get_lexemes("P279", entity, qual=False)])
	if superclasses:
		description = mkNP(aSg_Det,superclasses)
	else:
		classes = mkCN(w.and_Conj,[mkCN(cls) for cls in cnc.get_lexemes("P31", entity, qual=False)])
		if classes:
			description = mkNP(aSg_Det,mkCN(w.kind_of_N2,mkNP(classes)))
		else:
			description = None

	if description:
		fields = mkCN(w.and_Conj,[mkCN(field) for field in cnc.get_lexemes("P425", entity, qual=False)])
		if fields:
			description = mkNP(description,mkRS(mkRCl(which_RP,mkVP(mkVP(w.work_1_V),mkAdv(w.in_1_Prep,mkNP(theSg_Det,mkCN(mkCN(w.field_4_N),mkAdv(w.of_1_Prep, mkNP(fields)))))))))
		phr = mkPhr(mkUtt(mkS(mkCl(mkNP(aSg_Det,lexeme),description))),fullStopPunct)
		yield cnc.linearize(phr)
