import pgf
from wordnet import *
from nlg.util import *

def render(cnc, lexeme, entity):
    yield "<div class='infobox'><table border=1><tr><table>"
    for media,qual in get_medias("P18",entity):
        yield "<tr><td><img src='"+escape(media)+"' width=250/></td></tr>"
        break
    for media,qual in get_medias("P109",entity):
        yield "<tr><td><img src='"+escape(media)+"' width=250/></td></tr>"
        break
    yield "</table></tr></table></div>"

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
    

    # Property native language - P103
    native_language_qid = cnc.get_lexemes("P103",entity,qual=False)
    native_lang = []
    if native_language_qid:
        for qid in native_language_qid:
            native_lang.append(mkNP(qid))

    # Property languages spoken, written or signed - P1412
    other_langs = []
    for qid in cnc.get_lexemes("P1412",entity,qual=False):
        if qid not in native_language_qid:
            other_langs.append(mkNP(qid))

    if native_lang:
        num = singularNum if len(native_lang) == 1 else pluralNum
        native_lang = mkNP(w.and_Conj,native_lang)
        other_langs = mkNP(w.and_Conj,other_langs)
        if other_langs:
            # His/Her native lang(s) is/are [...] but he also speaks [...]
            phr = mkPhr(mkUtt(mkS(w.but_1_Conj,mkS(mkCl(mkNP(mkDet(pron,num), mkCN(w.native_2_A, w.language_1_N)), native_lang)),mkS(mkCl(mkNP(pron), mkVP(w.also_AdV,mkVP(w.speak_3_V2, other_langs)))))),fullStopPunct)
        else:
            # His/Her native lang(s) is/are [...]
            phr = mkPhr(mkUtt(mkS(mkCl(mkNP(mkDet(pron,num), mkCN(w.native_2_A, w.language_1_N)), native_lang))),fullStopPunct)
        yield " " + cnc.linearize(phr)
    elif other_langs:
        other_langs = mkNP(w.and_Conj,other_langs)
        # He/She speaks [...]
        phr = mkPhr(mkUtt(mkS(mkCl(mkNP(pron),mkVP(w.speak_3_V2, other_langs)))),fullStopPunct)
        yield " " + cnc.linearize(phr)
    

    # member of - P463
    institutions = []
    for qid,qual in get_items("P463",entity):
        inst = cnc.get_lex_fun(qid)
        if "P582" not in qual and inst != None:
            institutions.append(mkNP(inst))

    if institutions:
        # He/She is a member of [...]
        institutions = mkNP(w.and_Conj, list(institutions))
        phr = mkPhr(mkUtt(mkS(mkCl(mkNP(pron), mkNP(aSg_Det, w.PossNP(mkCN(w.member_4_N), institutions))))),fullStopPunct)
        yield " " + cnc.linearize(phr)

    yield "</p>"

    yield '<h2 class="gp-page-title">'+cnc.linearize(mkCN(w.personal_1_A,w.life_3_N))+'</h2>'
    yield "<p>"

    sisters  = []
    brothers = []
    for sibling in get_entities("P3373",entity,qual=False):
        name = cnc.get_person_name(sibling)
        if not name:
            continue
        if "Q6581072" in get_items("P21",sibling,qual=False):
            sisters.append(name)
        else:
            brothers.append(name)
    siblings = []
    if brothers:
        if len(brothers) == 1:
            det = aSg_Det
        elif len(brothers) < 10:
            det = mkDet(a_Quant,mkNum(mkNumeral(len(brothers))))
        else:
            det = mkDet(a_Quant,mkNum(len(brothers)))
        siblings.append(mkNP(det,mkCN(w.brother_1_N, mkNP(w.and_Conj,brothers))))
    if sisters:
        if len(sisters) == 1:
            det = aSg_Det
        elif len(sisters) < 10:
            det = mkDet(a_Quant,mkNum(mkNumeral(len(sisters))))
        else:
            det = mkDet(a_Quant,mkNum(len(sisters)))
        siblings.append(mkNP(det,mkCN(w.sister_1_N, mkNP(w.and_Conj,sisters))))
    siblings = mkNP(w.and_Conj, siblings)

    children = get_entities("P40",entity, qual=False)

    number_children_prop = get_quantities("P1971",entity)
    number = None
    for item in number_children_prop:
        number = int(item[0])

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
                           get_time_qualifier("P580",quals) or "X",
                           cnc.get_lexeme_qualifiers("P2842",quals),
                           get_time_qualifier("P582",quals),
                           get_item_qualifier("P1534",quals)) for spouse,quals in get_entities("P26",entity)],key=lambda p: p[1])
        for spouse,start,place,end,end_cause in spouses:
            occupation = cnc.get_lexemes("P106", spouse, qual=False)
            occupation = mkCN(occupation[0]) if occupation else None
            all_adjs, ds = cnc.get_demonyms("P27", spouse)
            if ds:
                ds = list(ds)[0] #converting the set to a list to access the first item
                if all_adjs:
                    description = mkCN(mkAP(ds), occupation) if occupation else None
                else:
                    description = occupation
            else:
                description = occupation

            child = None
            child_name = []
            if children:
                for kid in children:
                    if any(mother == spouse or father == spouse for mother in get_entities("P25", kid, qual=False) for father in get_entities("P22", kid, qual=False)):
                        child = cnc.get_person_name(kid)
                        if child:
                            child_name.append(child)
            number_children = len(child_name)
            child_name = mkNP(w.and_Conj, child_name)

            name = cnc.get_person_name(spouse)
            if name:
                if description:
                    name = mkCN(description, name)
                    vp = mkVP(w.marry_1_V2,mkNP(name))
                else:
                    vp = mkVP(w.marry_1_V2,name)
                if place:
                    vp = mkVP(vp,mkAdv(place[0]))
                stmt = mkS(useTense, mkCl(mkNP(pron), vp))
                if start:
                    start = str2date(start)
                    if start:
                        stmt = w.ExtAdvS(start,stmt)
                phr = mkPhr(mkUtt(stmt),fullStopPunct)
                yield " "+cnc.linearize(phr)
                
                if child_name:
                # They have X children: [list of names]
                    if number_children < 10:
                        det = mkDet(a_Quant,mkNum(mkNumeral(number_children)))
                    else:
                        det = mkDet(a_Quant,mkNum(number_children))
                    yield " " + cnc.linearize(mkPhr(mkUtt(mkS(mkCl(mkNP(w.they_Pron), mkVP(w.have_1_V2, mkNP(det, mkCN(w.child_2_N)))))))) + ":" + cnc.linearize(child_name) + "."
            
                if end and end_cause not in ["Q4", "Q99521170", "Q24037741"]:
                    if "Q6581072" in get_items("P21",spouse,qual=False):
                        spouse_pron = w.she_Pron
                    else:
                        spouse_pron = w.he_Pron
                    vp = mkVP(mkVP(w.divorce_2_V2,mkNP(spouse_pron)),str2date(end))
                    phr = mkPhr(mkUtt(mkS(useTense, mkCl(mkNP(pron), vp))),fullStopPunct)
                    yield " "+cnc.linearize(phr)
            
    spouse = get_entities("P26",entity, qual=False)
    if spouse and not children and number_children_prop:
        det = mkDet(a_Quant, mkNum(mkNumeral(number))) if number < 10 else mkDet(a_Quant, mkNum(number))
        phr = mkPhr(mkUtt(mkS(mkCl(mkNP(pron), mkVP(w.have_1_V2, mkNP(det, mkCN(w.child_2_N)))))), fullStopPunct)
        yield " " + cnc.linearize(phr)

    # If there is no spouse but there are children
    child = None
    child_name = []
    if not spouse:
        if children:
            for child in children:
                child = cnc.get_person_name(child)
                if child:
                    child_name.append(child)
        number_children = len(child_name)
        child_name = mkNP(w.and_Conj, child_name)

        if child_name:
            if number:
                det = mkDet(a_Quant, mkNum(mkNumeral(number))) if number < 10 else mkDet(a_Quant, mkNum(number))
            else:
                det = mkDet(a_Quant, mkNum(mkNumeral(number_children))) if number_children < 10 else mkDet(a_Quant, mkNum(number_children))

            if not number or number_children == number or number_children > number:
                yield " " + cnc.linearize(mkPhr(mkUtt(mkS(mkCl(mkNP(pron), mkVP(w.have_1_V2, mkNP(det, mkCN(w.child_2_N)))))))) + ":" + cnc.linearize(child_name) + "."
            elif number and number_children < number:
                phr = mkPhr(mkUtt(mkS(mkCl(mkNP(pron), mkVP(w.have_1_V2, mkNP(det, mkCN(w.child_2_N)))))), fullStopPunct)
                yield " " + cnc.linearize(phr)
        else:
            # No children name but number of children property
            if number:
                det = mkDet(a_Quant, mkNum(mkNumeral(number))) if number < 10 else mkDet(a_Quant, mkNum(number))
                phr = mkPhr(mkUtt(mkS(mkCl(mkNP(pron), mkVP(w.have_1_V2, mkNP(det, mkCN(w.child_2_N)))))), fullStopPunct)
                yield " " + cnc.linearize(phr)

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

    yield '<h2 class="gp-page-title">'+cnc.linearize(w.education_2_N)+'</h2>'
    yield "<p>"

    university = cnc.get_lexemes("P69",entity,qual=False)
    if university:
        universities = []
        for uni in university:
            universities.append(mkNP(uni))
        universities = mkNP(w.and_Conj, universities)

        # He/She graduated from [university name]
        phr = mkPhr(mkUtt(mkS(pastSimpleTense, mkCl(mkNP(pron), mkVP(mkVP(w.graduate_V), mkAdv(w.from_Prep, universities))))),fullStopPunct)
        yield " " + cnc.linearize(phr)

    yield "</p>"

    notable_works = get_entities(["P800"],entity,qual=False)
    if notable_works:
        yield '<h2 class="gp-page-title">'+cnc.linearize(mkUtt(mkNP(aPl_Det,mkCN(w.notable_2_A,w.work_2_N))))+'</h2>'
        yield "<ul>"
        for notable_work in notable_works:
            lbl = notable_work["labels"]
            lbl = lbl.get(cnc.lang) or lbl.get("en")
            if lbl:
                lbl = lbl["value"]
                yield "<li><a href=\"index.wsgi?id="+notable_work["id"]+"&lang="+cnc.lang+"\">"+lbl+"</a></li>"
        yield "</ul>"

    # award received:
    awards_dict = {}
    for qid, qual in get_items("P166",entity):
        award = cnc.get_lex_fun(qid)
        if not award:
            continue

        dates = awards_dict.setdefault(award,[])
        if "P585" in qual:
            date = get_time_qualifier("P585",qual)
            dates.append(date)

    if awards_dict:
        yield '<h2 class="gp-page-title">'+cnc.linearize(mkNP(aPl_Det,w.award_3_N))+'</h2>'

        # He/She received the following awards:
        yield '<p>'+cnc.linearize(mkPhr(mkUtt(mkS(pastSimpleTense, mkCl(mkNP(pron), mkVP(w.receive_1_V2, mkNP(thePl_Det,mkCN(w.following_2_A, w.award_3_N))))))))+':'
        
        # List of awards:
        if len(awards_dict) < 5:
            column_count = 1
        elif len(awards_dict) < 10:
            column_count = 2
        else:
            column_count = 4
        yield "<ul style='column-count: "+str(column_count)+"'>"
        for key,dates in awards_dict.items():
            if len(dates) > 1:
                # it extracts the year part (ex.: 2019) from each date string (ex.: '+2019-00-00T00:00:00Z') and constructs the date_string with years only
                date_string = ", ".join([date.split('-')[0].lstrip('+') for date in dates])
                yield "<li>"+cnc.linearize(key) + " (" + cnc.linearize(w.in_1_Prep) + " " + date_string +")"+"</li>"
            else:
                yield "<li>"+cnc.linearize(key)+"</li>"
        yield '</ul></p>'
