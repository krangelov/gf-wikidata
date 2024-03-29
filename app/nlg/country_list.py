import pgf

qids = ["Q16","Q17","Q20","Q27","Q28","Q29","Q30","Q31","Q32","Q33",
        "Q34","Q36","Q37","Q38","Q39","Q40","Q41","Q43","Q45","Q77",
        "Q79","Q96","Q114","Q115","Q117","Q142","Q145","Q148","Q155",
        "Q159","Q183","Q184","Q189","Q191","Q211","Q212","Q213",
        "Q214","Q215","Q217","Q218","Q219","Q221","Q222","Q224",
        "Q225","Q227","Q228","Q229","Q230","Q232","Q233","Q235",
        "Q236","Q237","Q238","Q241","Q242","Q244","Q252","Q258",
        "Q262","Q265","Q298","Q334","Q347","Q398","Q399","Q403",
        "Q408","Q414","Q419","Q423","Q424","Q574","Q657","Q664",
        "Q668","Q672","Q678","Q683","Q685","Q686","Q691","Q695",
        "Q697","Q702","Q709","Q710","Q711","Q712","Q717","Q730",
        "Q733","Q734","Q736","Q739","Q750","Q754","Q757","Q760",
        "Q763","Q766","Q769","Q774","Q778","Q781","Q783","Q784",
        "Q786","Q790","Q792","Q794","Q796","Q800","Q801","Q804",
        "Q805","Q810","Q811","Q813","Q817","Q819","Q822","Q826",
        "Q833","Q836","Q837","Q842","Q843","Q846","Q851","Q854",
        "Q858","Q863","Q865","Q869","Q874","Q878","Q881","Q884",
        "Q889","Q902","Q912","Q916","Q917","Q921","Q924","Q928",
        "Q929","Q945","Q948","Q953","Q954","Q958","Q962","Q963",
        "Q965","Q967","Q970","Q971","Q974","Q977","Q983","Q986",
        "Q1000","Q1005","Q1006","Q1007","Q1008","Q1009","Q1011",
        "Q1013","Q1014","Q1016","Q1019","Q1020","Q1025","Q1027",
        "Q1028","Q1029","Q1030","Q1032","Q1033","Q1036","Q1037",
        "Q1039","Q1041","Q1042","Q1044","Q1045","Q1049","Q1050",
        "Q29999","Q219060","Q756617"]

def render(cnc):
	yield "<ul>"
	for qid in qids:
		country = cnc.get_lex_fun(qid)
		if country != None:
			yield "<li>"+cnc.linearize(country)+"</li>"
		else:
			yield "<li>"+pgf.showExpr(country)+"</li>"
	yield "<ul>"
