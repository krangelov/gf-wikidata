import pgf
from wordnet import *
from nlg.util import *

def render(cnc, lexeme, entity):
    yield "<div class='infobox'><table border=1>"
    for media,qual in get_medias("P18",entity):
        yield "<tr><td><img src='"+escape(media)+"' width=250/></td></tr>"
    yield "</table></div>"

    description = mkCN(w.language_1_N)
    countries = mkNP(w.and_Conj,[mkNP(country) for country in cnc.get_lexemes("P17", entity, qual=False)])
    if countries:
        description = mkCN(mkAP(mkVPSlash(mkVPSlash(w.speak_3_V2),mkAdv(w.in_1_Prep,countries))),description)
    phr = mkPhr(mkUtt(mkS(mkCl(mkNP(lexeme),description))),fullStopPunct)
    yield cnc.linearize(phr)

    speakers_list = sorted(((speakers,get_time_qualifier("P585",quals) or "X") for speakers,quals in get_quantities("P1098",entity)),key=lambda p: p[1],reverse=True)
    if speakers_list:
        speakers = int(speakers_list[0][0])
        phr = mkPhr(mkUtt(mkS(mkCl(mkNP(mkNum(speakers),w.speaker_1_N)))),fullStopPunct)
        yield " "+cnc.linearize(phr)

    yield '<h2 class="gp-page-title">'+cnc.linearize(w.grammar_N)+'</h2>'

