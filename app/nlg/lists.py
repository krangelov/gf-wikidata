import pgf
from wordnet import *
from nlg.util import *


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


# Basic forms of government
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
# north korea -- single-party system (not correct but can't find another way to make it work)
sing_party_system = mkCN(w.single_3_A, mkCN(w.CompoundN(w.party_1_N,w.system_4_N)))
# semipres_democracy = mkCN(semipresidential w.democracy_2_N)
# parl_coprincipality = mkCN(w.parliamentary_2_A, coprincipality)
# direct_system = mkCN(directorial w.system_4_N)
# peoples_republic = mkCN(people's w.republic_2_N) --> Q465613
# west_system = mkCN(w.westminster_PN, w.system_4_N)


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
	("Q5440547", fed_parl_republic),   # federal parliamentary republic
	("Q50686", sing_party_system)	   # single-party system
	]


# Format comments
# Largest cities per sovereign country
largest_cities = [
	('Q1353', 26495000, 'Q668'), # Delhi 
	('Q8686', 24870895, 'Q148'), # Shanghai 
	('Q1354', 16800000, 'Q902'), # Dhaka 
	('Q406', 15462452, 'Q43'), # Istanbul 
	('Q8673', 15070000, 'Q1033'), # Lagos 
	('Q8660', 14910352, 'Q843'), # Karachi 
	('Q1490', 14047594, 'Q17'), # Tokyo 
	('Q649', 12455682, 'Q159'), # Moscow 
	('Q174', 12325232, 'Q155'), # São Paulo 
	('Q3838', 11855000, 'Q974'), # Kinshasa 
	('Q3630', 10562088, 'Q252'), # Jakarta 
	('Q1854', 10380000, 'Q881'), # Ho Chi Minh City 
	('Q2868', 9943800, 'Q419'), # Lima 
	('Q8684', 9668465, 'Q503585'), # Seoul 
	('Q8684', 9668465, 'Q884'), # Seoul 
	('Q85', 9606916, 'Q79'), # Cairo 
	('Q1489', 9209944, 'Q96'), # Mexico City 
	('Q84', 8908081, 'Q145'), # London 
	('Q60', 8804190, 'Q30'), # New York City 
	('Q3616', 8693706, 'Q794'), # Tehran 
	('Q3692', 8002100, 'Q851'), # Riyadh 
	('Q404817', 7816831, 'Q1065073'), # Shangqiu 
	('Q2841', 7743955, 'Q739'), # Bogotá 
	('Q37995', 7360703, 'Q836'), # Yangon 
	('Q1530', 6960000, 'Q796'), # Baghdad 
	('Q144663', 6645243, 'Q8733'), # Hengyang 
	('Q2887', 6257516, 'Q298'), # Santiago 
	('Q334', 5866139, 'Q334'), # Singapore 
	('Q1861', 5676648, 'Q869'), # Bangkok 
	('Q3870', 5545000, 'Q114'), # Nairobi 
	('Q1963', 5345000, 'Q1049'), # Khartoum 
	('Q1515', 4980000, 'Q1008'), # Abidjan 
	('Q3130', 4840600, 'Q408'), # Sydney 
	('Q1960', 4715000, 'Q924'), # Dar es Salaam 
	('Q34647', 4434827, 'Q258'), # Johannesburg 
	('Q244898', 4364124, 'Q865'), # New Taipei 
	('Q5838', 4273156, 'Q889'), # Kabul 
	('Q3805', 4007526, 'Q810'), # Amman 
	('Q64', 3677472, 'Q183'), # Berlin 
	('Q7903', 3499000, 'Q1028'), # Casablanca 
	('Q3561', 3415811, 'Q262'), # Algiers 
	('Q612', 3331420, 'Q878'), # Dubai 
	('Q170688', 3151676, 'Q750'), # Santa Cruz de la Sierra 
	('Q1486', 3120612, 'Q414'), # Buenos Aires 
	('Q3624', 3041002, 'Q115'), # Addis Ababa 
	('Q35178', 2989000, 'Q817'), # Kuwait City 
	('Q1475', 2960048, 'Q928'), # Quezon City 
	('Q2471', 2957000, 'Q805'), # Sanaa 
	('Q1899', 2952301, 'Q212'), # Kyiv 
	('Q220', 2872800, 'Q38'), # Rome 
	('Q18808', 2863000, 'Q423'), # Pyongyang 
	('Q172', 2794356, 'Q16'), # Toronto 
	('Q132830', 2768436, 'Q1009'), # Douala 
	('Q43509', 2723665, 'Q736'), # Guayaquil 
	('Q269', 2571668, 'Q265'), # Tashkent 
	('Q3766', 2503000, 'Q858'), # Damascus 
	('Q1563', 2492618, 'Q241'), # Havana 
	('Q3897', 2487444, 'Q916'), # Luanda 
	('Q3881', 2467563, 'Q953'), # Lusaka 
	('Q3777', 2453496, 'Q965'), # Ouagadougou 
	('Q3820', 2421354, 'Q822'), # Beirut 
	('Q3761', 2388000, 'Q117'), # Accra 
	('Q9248', 2300500, 'Q227'), # Baku 
	('Q1533', 2245744, 'Q717'), # Caracas 
	('Q3792', 2188376, 'Q945'), # Lomé 
	('Q3921', 2150000, 'Q954'), # Harare 
	('Q90', 2145906, 'Q142'), # Paris 
	('Q1850', 2129371, 'Q424'), # Phnom Penh 
	('Q2449', 2120000, 'Q1045'), # Mogadishu 
	('Q3703', 2009109, 'Q912'), # Bamako 
	('Q2280', 1995471, 'Q184'), # Minsk 
	('Q56036', 1984837, 'Q2415901'), # West Berlin 
	('Q1865', 1982100, 'Q833'), # Kuala Lumpur 
	('Q1741', 1973403, 'Q40'), # Vienna 
	('Q35493', 1916822, 'Q232'), # Almaty 
	('Q188693', 1895973, 'Q1020'), # Blantyre 
	('Q270', 1860281, 'Q36'), # Warsaw 
	('Q3844', 1827000, 'Q971'), # Brazzaville 
	('Q19660', 1716983, 'Q218'), # Bucharest 
	('Q1781', 1706851, 'Q28'), # Budapest 
	('Q3238', 1682725, 'Q783'), # Tegucigalpa 
	('Q3894', 1680600, 'Q1036'), # Kampala 
	('Q3733', 1667864, 'Q1006'), # Conakry 
	('Q2074197', 1659440, 'Q403'), # City of Belgrade 
	('Q37100', 1470100, 'Q664'), # Auckland 
	('Q3718', 1438725, 'Q1041'), # Dakar 
	('Q3826', 1421409, 'Q842'), # Muscat 
	('Q23430', 1396288, 'Q711'), # Ulaanbaatar 
	('Q472', 1383435, 'Q219'), # Sofia 
	('Q1085', 1357326, 'Q213'), # Prague 
	('Q42763', 1343423, 'Q786'), # Santiago de los Caballeros 
	('Q1335', 1319108, 'Q77'), # Montevideo 
	('Q3579', 1293016, 'Q1016'), # Tripoli 
	('Q56037', 1279212, 'Q16957'), # East Berlin 
	('Q3915', 1275207, 'Q1019'), # Antananarivo 
	('Q240', 1218255, 'Q31'), # Brussels-Capital Region 
	('Q1555', 1213651, 'Q774'), # Guatemala City 
	('Q3889', 1191613, 'Q1029'), # Maputo 
	('Q3861', 1186023, 'Q846'), # Doha 
	('Q3859', 1156663, 'Q1037'), # Kigali 
	('Q9361', 1120827, 'Q813'), # Bishkek 
	('Q994', 1118035, 'Q230'), # Tbilisi 
	('Q3659', 1092066, 'Q657'), # N'Djamena
	('Q3688', 1077169, 'Q1025'), # Nouakchott 
	('Q1953', 1075800, 'Q399'), # Yerevan 
	('Q158467', 1069276, 'Q33296'), # Gwalior 
	('Q3674', 1026848, 'Q1032'), # Niamey 
	('Q3748', 1021762, 'Q1014'), # Monrovia 
	('Q34261', 987310, 'Q790'), # Port-au-Prince 
	('Q1754', 978770, 'Q34'), # Stockholm 
	('Q3642', 963000, 'Q986'), # Asmara 
	('Q3780', 951000, 'Q1044'), # Freetown 
	('Q3274', 937489, 'Q811'), # Managua 
	('Q727', 921468, 'Q55'), # Amsterdam 
	('Q1218', 919438, 'Q801'), # Jerusalem 
	('Q223761', 903887, 'Q797422'), # Bobo-Dioulasso 
	('Q223761', 903887, 'Q797440'), # Bobo-Dioulasso 
	('Q3832', 889231, 'Q929'), # Bangui 
	('Q3306', 880691, 'Q804'), # Panama City 
	('Q9365', 863400, 'Q863'), # Dushanbe 
	('Q3037', 845767, 'Q837'), # Kathmandu 
	('Q23438', 828100, 'Q874'), # Ashgabat 
	('Q3825', 797003, 'Q1000'), # Libreville 
	('Q131301', 775404, 'Q1747689'), # Homs 
	('Q1435', 767131, 'Q224'), # Zagreb 
	('Q168652', 760000, 'Q34754'), # Hargeisa 
	('Q35381', 752993, 'Q854'), # Colombo 
	('Q585', 709037, 'Q20'), # Oslo 
	('Q43595', 679012, 'Q962'), # Cotonou 
	('Q31926034', 666880, 'Q175276'), # Zaragoza City 
	('Q31926034', 666880, 'Q199442'), # Zaragoza City 
	('Q31926034', 666880, 'Q29'), # Zaragoza City 
	('Q1757', 664921, 'Q33'), # Helsinki 
	('Q1524', 664046, 'Q41'), # Athens 
	('Q3854', 658859, 'Q967'), # Bujumbura 
	('Q193250', 653337, 'Q217169'), # Bulawayo 
	('Q193250', 653337, 'Q750583'), # Bulawayo 
	('Q193250', 653337, 'Q890120'), # Bulawayo 
	('Q1748', 644431, 'Q35'), # Copenhagen 
	('Q21197', 639000, 'Q217'), # Chișinău 
	('Q1773', 605802, 'Q211'), # Riga 
	('Q3604', 603900, 'Q977'), # Djibouti 
	('Q3572', 602560, 'Q948'), # Tunis 
	('Q216', 581475, 'Q37'), # Vilnius 
	('Q34692', 580000, 'Q766'), # Kingston 
	('Q1761', 553165, 'Q27'), # Dublin 
	('Q597', 545923, 'Q45'), # Lisbon 
	('Q384', 526502, 'Q221'), # Skopje 
	('Q1947', 525953, 'Q958'), # Juba 
	('Q2933', 524190, 'Q733'), # Asunción 
	('Q3909', 519186, 'Q1013'), # Maseru 
	('Q47492', 515556, 'Q219060'), # Gaza City 
	('Q3739', 492004, 'Q1007'), # Bissau 
	('Q148062', 481300, 'Q1121819'), # Zarqa 
	('Q1780', 475503, 'Q214'), # Bratislava 
	('Q200340', 451100, 'Q129286'), # Udaipur 
	('Q1770', 438341, 'Q191'), # Tallinn 
	('Q72', 436332, 'Q39'), # Zürich 
	('Q3935', 431000, 'Q1030'), # Windhoek 
	('Q19689', 418495, 'Q222'), # Tirana 
	('Q41211', 342259, 'Q1183'), # San Juan 
	('Q3070', 342188, 'Q800'), # San José 
	('Q3856', 330000, 'Q23681'), # Nicosia 
	('Q3856', 330000, 'Q229'), # Nicosia 
	('Q36526', 317374, 'Q691'), # Port Moresby 
	('Q3110', 316090, 'Q792'), # San Salvador 
	('Q893274', 315351, 'Q124943'), # Bor 
	('Q3818', 297000, 'Q983'), # Malabo 
	('Q588', 285711, 'Q207272'), # Katowice 
	('Q588', 285711, 'Q211274'), # Katowice 
	('Q588', 285711, 'Q38872'), # Katowice 
	('Q437', 284293, 'Q215'), # Ljubljana 
	('Q11194', 275524, 'Q225'), # Sarajevo 
	('Q2467', 274400, 'Q778'), # Nassau 
	('Q188894', 266784, 'Q12560'), # Kütahya 
	('Q128147', 260200, 'Q179876'), # Kingston upon Hull 
	('Q3919', 246325, 'Q963'), # Gaborone 
	('Q3001', 223757, 'Q730'), # Paramaribo 
	('Q9310', 222323, 'Q574'), # Dili 
	('Q47837', 217732, 'Q40362'), # Laayoune 
	('Q10717', 200500, 'Q734'), # Georgetown 
	('Q25270', 198897, 'Q1246'), # Prishtina 
	('Q192213', 194300, 'Q193714'), # Holon 
	('Q1001104', 185082, 'Q15180'), # Temirtau 
	('Q1001104', 185082, 'Q34266'), # Temirtau 
	('Q3751', 159050, 'Q1011'), # Praia 
	('Q3882', 157474, 'Q398'), # Manama 
	('Q23564', 150977, 'Q236'), # Podgorica 
	('Q132679', 150000, 'Q25279'), # Willemstad 
	('Q3929', 149194, 'Q1027'), # Port Louis 
	('Q1764', 135688, 'Q189'), # Reykjavík 
	('Q132572', 133807, 'Q907112'), # Tiraspol 
	('Q9347', 133019, 'Q826'), # Malé 
	('Q1842', 132780, 'Q32'), # Luxembourg 
	('Q926426', 130495, 'Q4224856'), # Kozan 
	('Q750443', 124000, 'Q819'), # Savannakhet 
	('Q383622', 119848, 'Q870055'), # Pāksē 
	('Q383622', 119848, 'Q1320058'), # Pāksē 
	('Q174684', 110979, 'Q28513'), # Tuzla 
	('Q495730', 110508, 'Q1050'), # Manzini 
	('Q36168', 110000, 'Q244'), # Bridgetown 
	('Q345204', 106277, 'Q6250'), # Dakhla 
	('Q38807', 88271, 'Q712'), # Suva 
	('Q40921', 84520, 'Q685'), # Honiara 
	('Q1444575', 83489, 'Q754'), # Chaguanas 
	('Q185289', 81308, 'Q121932'), # Pernik 
	('Q185289', 81308, 'Q147909'), # Pernik 
	('Q185289', 81308, 'Q815731'), # Pernik 
	('Q9270', 79185, 'Q917'), # Thimphu 
	('Q3901', 74749, 'Q970'), # Moroni 
	('Q3932', 71868, 'Q1039'), # São Tomé 
	('Q83531', 71501, 'Q878818'), # Bitlis 
	('Q41699', 70000, 'Q760'), # Castries 
	('Q3476', 69439, 'Q172579'), # L’Aquila 
	('Q40811', 64441, 'Q139319'), # Sukhumi 
	('Q40811', 64441, 'Q154667'), # Sukhumi 
	('Q40811', 64441, 'Q245160'), # Sukhumi 
	('Q40811', 64441, 'Q307041'), # Sukhumi 
	('Q40811', 64441, 'Q325493'), # Sukhumi 
	('Q40811', 64441, 'Q330756'), # Sukhumi 
	('Q40811', 64441, 'Q545205'), # Sukhumi 
	('Q40811', 64441, 'Q1069959'), # Sukhumi 
	('Q40811', 64441, 'Q55659450'), # Sukhumi 
	('Q40811', 64441, 'Q12544'), # Sukhumi 
	('Q131233', 63439, 'Q710'), # South Tarawa 
	('Q187807', 58367, 'Q80702'), # San Fernando 
	('Q108223', 57169, 'Q242'), # Belize City 
	('Q842810', 57035, 'Q689837'), # Smara 
	('Q216363', 56988, 'Q133356'), # Rîbnița 
	('Q216363', 56988, 'Q172107'), # Rîbnița 
	('Q216363', 56988, 'Q203493'), # Rîbnița 
	('Q216363', 56988, 'Q243610'), # Rîbnița 
	('Q216363', 56988, 'Q1508143'), # Rîbnița 
	('Q216363', 56988, 'Q2305208'), # Rîbnița 
	('Q37806', 51437, 'Q686'), # Port Vila 
	('Q9279', 50000, 'Q921'), # Bandar Seri Begawan 
	('Q129352', 49848, 'Q244165'), # Stepanakert 
	('Q95895695', 48500, 'Q70972'), # Free Imperial City of Strasbourg 
	('Q95895695', 48500, 'Q12548'), # Free Imperial City of Strasbourg 
	('Q571215', 43337, 'Q541455'), # Suakin 
	('Q214681', 40017, 'Q323904'), # Panaji 
	('Q36260', 37708, 'Q683'), # Apia 
	('Q131243', 34980, 'Q21203'), # Oranjestad 
	('Q1410', 34003, 'Q1410'), # Gibraltar 
	('Q147738', 33522, 'Q785'), # Saint Helier 
	('Q3726', 31356, 'Q1005'), # Banjul 
	('Q79863', 30432, 'Q23427'), # Tskhinvali 
	('Q208169', 30000, 'Q208169'), # Republic of Ragusa 
	('Q12919', 30000, 'Q709'), # Majuro 
	('Q172996', 27704, 'Q5785'), # George Town 
	('Q3940', 26450, 'Q1042'), # Victoria 
	('Q36262', 24451, 'Q781'), # Saint John's
	('Q39583', 24356, 'Q233'), # Birkirkara 
	('Q38834', 23221, 'Q678'), # Nuku'alofa
	('Q1863', 22151, 'Q228'), # Andorra la Vella 
	('Q1899332', 19197, 'Q407199'), # Qabatiya 
	('Q226', 18326, 'Q223'), # Nuuk 
	('Q1001326', 17394, 'Q682001'), # Pyskowice 
	('Q1001326', 17394, 'Q7318'), # Pyskowice 
	('Q1001326', 17394, 'Q27306'), # Pyskowice 
	('Q1001326', 17394, 'Q41304'), # Pyskowice 
	('Q1001326', 17394, 'Q43287'), # Pyskowice 
	('Q36281', 16582, 'Q784'), # Roseau 
	('Q41474', 16532, 'Q757'), # Kingstown 
	('Q2078085', 14931, 'Q964024'), # Fălești 
	('Q2078085', 14931, 'Q10957559'), # Fălești 
	('Q51681', 14477, 'Q11703'), # Charlotte Amalie 
	('Q640493', 13951, 'Q1206012'), # Kępno 
	('Q837170', 13278, 'Q131964'), # Gura Humorului 
	('Q837170', 13278, 'Q153136'), # Gura Humorului 
	('Q41295', 13220, 'Q763'), # Basseterre 
	('Q527748', 8744, 'Q695'), # Koror 
	('Q3456410', 7956, 'Q435583'), # Republic of Mulhouse 
	('Q236673', 7449, 'Q31354462'), # Gali 
	('Q42751', 6227, 'Q702'), # Palikir 
	('Q34126', 6025, 'Q672'), # Funafuti 
	('Q1844', 5668, 'Q347'), # Vaduz 
	('Q41547', 4315, 'Q769'), # St. George's
	('Q211318', 4107, 'Q2914461'), # Pitsunda 
	('Q1848', 4040, 'Q238'), # San Marino 
	('Q30985', 3686, 'Q23635'), # Hamilton 
	('Q1722578', 2547, 'Q459780'), # Kaloyanovo 
	('Q993064', 2000, 'Q25230'), # Saint Anne 
	('Q1411798', 1524, 'Q3113481'), # Coșbuc 
	('Q30958', 1338, 'Q26273'), # Philipsburg 
	('Q429059', 1190, 'Q2071857'), # Dvin 
	('Q429059', 1190, 'Q2571688'), # Dvin 
	('Q939009', 1183, 'Q2685298'), # Nițchidorf 
	('Q30994', 1067, 'Q25228'), # The Valley 
	('Q31026', 747, 'Q697'), # Yaren District 
	('Q30970', 714, 'Q192184'), # Jamestown 
	('Q642787', 541, 'Q36823'), # Atafu 
	('Q237', 453, 'Q237'), # Vatican City 
	('Q998529', 361, 'Q154195'), # Buchhorn 
	('Q30990', 0, 'Q13353') # Plymouth
	]


# Continents
the_world = mkNP(theSg_Det, mkCN(w.world_1_N))
europe = mkNP(w.europe_1_LN)
asia = mkNP(w.asia_1_LN)
africa = mkNP(w.africa_LN)
north_america = mkNP(w.north_america_1_LN)
south_america = mkNP(w.south_america_1_LN)
insular_oceania = mkNP(w.insular_oceania_LN)

# Top 5 highest life expectancies per continent / the world
top = [
	("Q238", 85.41707, the_world),        # San Marino
	#("Q17", 83.98488, the_world),         # Japan
	#("Q16", 83.62, the_world),            # Canada
	#("Q183", 80.8, the_world),            # Germany
	#("Q39", 82.89756, the_world),         # Switzerland
	("Q238", 85.41707, europe),           # San Marino
	#("Q183", 83.3, europe),               # Germany
	#("Q39", 82.89756, europe),            # Switzerland
	#("Q347", 82.6561, europe),            # Liechtenstein
	#("Q38", 82.5439, europe),             # Italy
	("Q17", 83.98488, asia),              # Japan
	#("Q334", 82.79512, asia),             # Singapore
	#("Q801", 82.6, asia),                 # Israel
	#("Q884", 82.02439, asia),             # South Korea
	#("Q229", 80.508, asia),               # Cyprus
	("Q262", 76.078, africa),             # Algeria
	#("Q1028", 75.821, africa),            # Morocco
	#("Q948", 75.731, africa),             # Tunisia
	#("Q1027", 74.39488, africa),          # Mauritius
	#("Q1042", 74.30976, africa),          # Seychelles
	("Q16", 83.62, north_america),        # Canada
	#("Q800", 79.831, north_america),      # Costa Rica
	#("Q241", 79.742, north_america),      # Cuba
	#("Q30", 78.69024, north_america),     # United States
	#("Q804", 78.001, north_america),      # Panama
	("Q298", 80, south_america),          # Chile
	#("Q77", 77.493, south_america),       # Uruguay
	#("Q414", 76.577, south_america),      # Argentina
	#("Q736", 76.327, south_america),      # Ecuador
	#("Q155", 75.723, south_america),      # Brazil
	("Q408", 82.5, insular_oceania),      # Australia
	#("Q664", 81.61244, insular_oceania),  # New Zealand
	#("Q683", 75.013, insular_oceania),    # Samoa
	#("Q252", 73.515, insular_oceania),    # Indonesia
	#("Q678", 73.029, insular_oceania)     # Tonga
	]


# Top 5 lowest life expectancies per continent / the world
bottom = [ # sorted from lower to higher life expectancy
	("Q1044", 51.835, the_world),         # Sierra Leone
	#("Q929", 52.171, the_world),          # Central African Republic
	#("Q657", 52.903, the_world),          # Chad
	#("Q1033", 53.428, the_world),         # Nigeria
	#("Q1008", 53.582, the_world),         # Ivory Coast
	("Q212", 71.47634, europe),           # Ukraine
	#("Q159", 71.59293, europe),           # Russia
	#("Q217", 71.61, europe),              # Moldova
	#("Q227", 72.026, europe),             # Azerbaijan
	#("Q232", 72.3, europe),               # Kazakhstan
	("Q889", 63.673, asia),               # Afghanistan
	#("Q805", 64.953, asia),               # Yemen
	#("Q819", 66, asia),                   # Laos
	#("Q874", 67.835, asia),               # Turkmenistan
	#("Q574", 68.881, asia),               # East Timor
	("Q1044", 51.835, africa),            # Sierra Leone
	#("Q929", 52.171, africa),             # Central African Republic
	#("Q657", 52.903, africa),             # Chad
	#("Q1033", 53.428, africa),            # Nigeria
	#("Q1008", 53.582, africa),            # Ivory Coast
	("Q790", 63.33, north_america),       # Haiti
	#("Q242", 70.384, north_america),      # Belize
	#("Q754", 70.673, north_america),      # Trinidad and Tobago
	#("Q763", 71.33659, north_america),    # Saint Kitts and Nevis	
	#("Q757", 73.179, north_america),      # Saint Vincent and the Grenadines
	("Q734", 66.65, south_america),       # Guyana
	#("Q750", 69.125, south_america),      # Bolivia
	#("Q730", 71.405, south_america),      # Suriname
	#("Q733", 73.12, south_america),       # Paraguay
	#("Q739", 74.381, south_america),      # Colombia
	("Q709", 65.23902, insular_oceania),  # Marshall Islands
	#("Q691", 65.544, insular_oceania),    # Papua New Guinea
	#("Q710", 68.46, insular_oceania),     # Kiribati
	#("Q695", 69.12927, insular_oceania),  # Palau
	#("Q702", 69.195, insular_oceania)     # Federated States of Micronesia
	]



# There are some VAT products that have no lexeme (ex.: accommodation), and hence, are not listed
# when generating the VAT sentence. The idea is to create a list like form_of_government above that includes the qid
# of the product and its corresponding lexeme.
assistive_technology = mkCN(w.assistive_A, w.technology_1_N)
air_transport = mkCN(w.CompoundN(w.air_9_N, w.transport_1_N))
accommodation = mkCN(w.accommodation_5_N)
clothing = mkCN(w.clothing_N)
sewerage = mkCN(w.sewerage_2_N)
medicinal_product = mkCN(w.medicinal_A, w.product_1_N)
beauty_services = mkCN(w.CompoundN(w.beauty_1_N, w.service_1_N))
public_transport = mkCN(w.public_1_A, w.transport_1_N)
wellbeing_activities = mkCN(w.CompoundN(w.well_being_N, w.activity_1_N))


# The dict indicates when a product needs to be used in plural (language-dependent), where True == plural
VAT_applies_to_part = [
	("Q688498", assistive_technology, {'en': False, 'es': False, 'fr': True}),
	("Q1757562", air_transport, {'en': False, 'es': False, 'fr': False}),
    ("Q29584320", accommodation, {'en': False, 'es': False, 'fr': False}),
    ("Q11460", clothing, {'en': False, 'es': False, 'fr': True}),
    ("Q21040870", sewerage, {'en': False, 'es': False, 'fr': False}),
    ("Q12034612", medicinal_product, {'en': False, 'es': True, 'fr': True}),
    ("Q29586123", beauty_services, {'en': True, 'es': True, 'fr': True}),   # Hairdressing and other beauty treatment
    ("Q178512", public_transport, {'en': False, 'es': False, 'fr': False}),
    ("Q29586130", wellbeing_activities, {'en': True, 'es': True, 'fr': True}), # Physical well-being activities
]


# List of all the VAT products with lexemes
vat_products_in_use = [
    				("food_1_N", {'en': False, 'es': False, 'fr': True}),
                    ("plant_2_N", {'en': True, 'es': True, 'fr': True}),
                    ("firewood_N",  {'en': False, 'es': False, 'fr': False}),
                    ("formula_6_N", {'en': False, 'es': False, 'fr': False}),
                    ("flour_N", {'en': False, 'es': False, 'fr': False}),
                    ("malt_3_N", {'en': False, 'es': False, 'fr': False}),
                    ("starch_1_N", {'en': False, 'es': False, 'fr': False}),
                    ("drinking_water_N", {'en': False, 'es': False, 'fr': False}),
                    ("medication_1_N", {'en': False, 'es': True, 'fr': False}),
                    ("ticket_1_N", {'en': True, 'es': True, 'fr': True}),
                    ("library_1_N", {'en': True, 'es': True, 'fr': True}),
                    ("periodical_N", {'en': True, 'es': True, 'fr': True}),
                    ("water_1_N", {'en': False, 'es': False, 'fr': False}),
                    ("transport_1_N", {'en': False, 'es': False, 'fr': False}),
                    ("catering_N", {'en': False, 'es': False, 'fr': False}),
                    ("margarine_N", {'en': False, 'es': False, 'fr': False}),
                    ("hotel_N", {'en': True, 'es': True, 'fr': True}),
                    ("book_1_N", {'en': True, 'es': True, 'fr': True}),
                    ("newspaper_3_N", {'en': True, 'es': True, 'fr': True}),
                    ("culture_6_N", {'en': False, 'es': False, 'fr': False}),
                    ("sport_1_N", {'en': False, 'es': False, 'fr': False}),
                    ("rental_2_N", {'en': True, 'es': True, 'fr': True}),
                    ("healthcare_2_N", {'en': False, 'es': False, 'fr': False}),
                    ("garment_N", {'en': True, 'es': True, 'fr': True}),
                    ("tampon_N", {'en': True, 'es': True, 'fr': True}),
                     ]




# this list contains (qid, w.lexeme) for some organizations
org_qid_lexeme = [
    #('Q1065', w.un_PN), # United Nations
    ('Q7817', w.who_PN), # World Health Organization
    #('Q17495', w.upu_PN), #Universal Postal Union
    #('Q842490', w.opcw_PN), #Organization for the Prohibition of Chemical Weapons
    #('Q7825', w.wto_PN), # World Trade Organization
	#('Q656801', w.ifc_PN), # International Finance Corporation
    ]


# list of all organizations of which the countries are current/former members (and the number of members)
organizations_count = [
    ('Interpol', 194),
	('United Nations', 194),
	('World Health Organization', 192),
	('UNESCO', 191),
	('Universal Postal Union', 189),
	('Organisation for the Prohibition of Chemical Weapons', 189),
	('International Telecommunication Union', 189),
	('International Bank for Reconstruction and Development', 187),
	('International Finance Corporation', 183),
	('World Meteorological Organization', 180),
	('Multilateral Investment Guarantee Agency', 179),
	('International Development Association', 171),
	('World Trade Organization', 156),
	('International Centre for Settlement of Investment Disputes', 149),
	('Group on Earth Observations', 104),
	('International Hydrographic Organization', 86),
	('African Development Bank', 81),
	('Organisation of African, Caribbean and Pacific States', 77),
	('International Civil Defence Organisation', 75),
	('Asian Development Bank', 64),
	('Commonwealth of Nations', 56), # lexeme is commonwealth_3_N but it should be commonwealth_PN
	('Organisation of Islamic Cooperation', 56),
	('Organization for Security and Co-operation in Europe', 55),
	('African Union', 54),
	('Organisation internationale de la Francophonie', 51),
	('Nuclear Suppliers Group', 48),
	('Council of Europe', 45),
	('African Union – United Nations Hybrid Operation in Darfur', 44),
	('Eurocontrol', 43),
	('Australia Group', 40),
	('Visa Waiver Program', 38),
	('Alliance of Small Island States', 37),
	('Organization for Economic Cooperation and Development', 36),
	('Organization of American States', 35),
	('Missile Technology Control Regime', 35),
	('Treaty on Open Skies', 34),
	('Agency for the Prohibition of Nuclear Weapons in Latin America and the Caribbean', 33),
	('North Atlantic Treaty Organization', 30),
	('International Energy Agency', 29),
	('Movement Coordination Centre Europe', 29),
	('European Union', 28),
	('Schengen Area', 26),
	('ASEAN Regional Forum', 25),
	('Arab League', 22),
	('Arab Monetary Fund', 22),
	('Caribbean Development Bank', 22),
	('AFRISTAT', 22),
	('Arab Fund for Economic and Social Development', 21),
	('Asia-Pacific Economic Cooperation', 20),
	('European Space Agency', 19),
	('G20', 19),
	('International Centre for Migration Policy Development', 19),
	('Arab Bank for Economic Development in Africa', 18),
	('OHADA', 17),
	('Southern African Development Community', 15),
	('Economic Community of West African States', 15),
	('European Southern Observatory', 15),
	('European Payments Union', 15),
	('Caribbean Disaster Emergency Management Agency', 14),
	('Caribbean Community', 14),
	('Organization of the Petroleum Exporting Countries', 13),
	('Antarctic Treaty System', 13),
	('Commonwealth of Independent States', 12),
	('ASEAN', 12),
	('Union of South American Nations', 12),
	('Council of the Baltic Sea States', 12),
	('Organization of the Black Sea Economic Cooperation', 12),
	('Central American Bank for Economic Integration', 12),
	('Strategic Airlift Capability', 12),
	('Economic Community of Central African States', 11),
	('United Nations Security Council', 9),
	('Arctic Council', 9),
	('Andean Community', 9),
	('Collective Security Treaty Organization', 9),
	('Community of Portuguese Language Countries', 9),
	('Commonwealth of Independent States Free Trade Area', 9),
	('International Atomic Energy Agency', 8),
	('Shanghai Cooperation Organisation', 8),
	('International Regional Organization for Agricultural Health', 8),
	('Gulf of Guinea Commission', 8),
	('COMECON', 8),
	('states with nuclear weapons', 8),
	('Mercosur', 7),
	('G8', 7),
	('Food and Agriculture Organization', 7),
	('Bay of Bengal Initiative for Multi-Sectoral Technical and Economic Cooperation', 7),
	('International Fund for Agricultural Development', 7),
	('Organization of Turkic States', 7),
	('International Renewable Energy Agency', 7),
	('Southeast Asia Treaty Organization', 7),
	('World Intellectual Property Organization', 7),
	('European Air Transport Command', 7),
	('International Civil Aviation Organization', 7),
	('International Monetary Fund', 6),
	('International Criminal Court', 6),
	('League of Nations', 6),
	('Organisation for Joint Armament Cooperation', 6),
	('African Groundnut Council', 6),
	('Barents Euro-Arctic Council', 6),
	('International Maritime Organization', 6),
	('Nordic Battle Group', 6),
	('Bank of Central African States', 6),
	('Nordic Council', 6),
	('World Tourism Organization', 5),
	('Warsaw Pact', 5),
	("Conseil de l'Entente", 5),
	('Non-Aligned Movement', 5),
	('The Technical Cooperation Program', 5),
	('Combined Communications-Electronics Board', 5),
	('Air Force Interoperability Council', 5),
	('AUSCANNZUKUS', 5),
	('Arab Maghreb Union', 5),
	('GUAM Organization for Democracy and Economic Development', 5),
	('ABCANZ Armies', 5),
	('BRICS', 5),
	('Central Asian Cooperation Organization', 5),
	('Central American Common Market', 5),
	('United Nations Conference on Trade and Development', 5),
	('Southern African Customs Union', 5),
	('Community of Latin American and Caribbean States', 5),
	('International Labour Organization', 4),
	('CERN', 4),
	('International Olympic Committee', 4),
	('Carbon Neutrality Coalition', 4),
	('European Bank for Reconstruction and Development', 4),
	('International Organization for Migration', 4),
	('United Nations Industrial Development Organization', 4),
	('Bank for International Settlements', 4),
	('Visegrád Group', 4),
	('European Free Trade Association', 4),
	('European Coal and Steel Community', 4),
	('Five Eyes', 4),
	('Mano River Union', 4),
	('Indian Ocean Commission', 4),
	('European Economic Area', 3),
	('International Red Cross and Red Crescent Movement', 3),
	('European Economic Community', 3),
	('Benelux', 3),
	('Rio Group', 3),
	('BRIC', 3),
	('Baltic Assembly', 3),
	('Caribbean Free Trade Association', 3),
	('Group of 77', 3),
	('ANZUK', 3),
	('Cooperation Council for the Arab States of the Gulf', 3),
	('Union for the Mediterranean', 3),
	('North American Free Trade Agreement', 3),
	('International Federation of Red Cross and Red Crescent Societies', 3),
	('Bolivarian Alliance for the Americas', 2),
	('International Organization for Standardization', 2),
	('International Military Sports Council', 2),
	('G4 nations', 2),
	('Intelsat', 2),
	('Montenegro–Ukraine Free Trade Area', 2),
	('Latin American Integration Association', 2),
	('World Customs Organization', 2),
	('Weimar Triangle', 2),
	('Anzus', 2),
	('Eastern Partnership', 2),
	('Western European Union', 2),
	('European Convention on Human Rights', 2),
	('Interparliamentary Union', 2),
	('Union State', 2),
	('Belgium–Luxembourg Economic Union', 2),
	('Global Biodiversity Information Facility', 2),
	('Dutch Language Union', 2),
	('South Asian Association for Regional Cooperation', 2),
	('Latin Union', 2),
	('Inter-American Development Bank', 2),
	('AUKUS', 2),
	('Permanent Court of Arbitration', 2),
	('European Atomic Energy Community', 1),
	('Eurozone', 1),
	('World Bank', 1),
	('Kalmar Union', 1),
	('Union between Sweden and Norway', 1),
	('International Coffee Organization', 1),
	('South Atlantic Peace and Cooperation Zone', 1),
	('United Nations Economic Commission for Latin America and the Caribbean', 1),
	('Maghreb', 1),
	('National Aeronautics and Space Administration', 1),
	('Lomé Convention', 1),
	('Lublin Triangle', 1),
	('Group of 15', 1),
	('MIKTA', 1),
	('International Chamber of Commerce', 1),
	('1990 Schengen Convention', 1),
	('World Federation of Trade Unions', 1),
	('International Commission for the Protection of the Danube River', 1),
	('United Nations Truce Supervision Organization', 1),
	('Netherlands-Indonesian Union', 1),
	('United Nations Economic Commission for Europe', 1),
	('Partnership for Peace', 1),
	('EFTA Court', 1),
	('Community of Sahel-Saharan States', 1),
	('Latin American and the Caribbean Economic System', 1),
	('Amazon Cooperation Treaty Organization', 1),
	('member states of the Organization of Ibero-American States', 1),
	('East Asia Summit', 1),
	('European Common Aviation Area', 1),
	('Ibero-American Summit', 1),
	('Caribbean Forum', 1),
	('Latin American Parliament', 1),
	('Arab Information and Communication Technologies Organization', 1),
	('Eurasian Economic Community', 1),
	('American Convention on Human Rights', 1),
	('Summits of the Americas', 1),
	('Organization of Ibero-American States', 1),
	('Comprehensive Nuclear-Test-Ban Treaty Organization', 1),
	('United Nations Convention to Combat Desertification', 1),
	('Central European Free Trade Agreement', 1),
	('Inter-American Tropical Tuna Commission', 1),
	('ABC nations', 1),
	('Association of National Olympic Committees', 1),
	('Summit of South American-Arab Countries', 1),
	('Economic, Monetary and Social Union', 1),
	('Western and Central Pacific Fisheries Commission', 1),
	('FIFA', 1),
	('Commission for the Conservation of Southern Bluefin Tuna', 1),
	('Berne Convention for the Protection of Literary and Artistic Works', 1),
	('United Nations Convention on the Law of the Sea', 1),
	('United Nations Framework Convention on Climate Change', 1),
	('General Agreement on Tariffs and Trade', 1),
	('Conference on Disarmament', 1),
	('Organisation of African Unity', 1),
	('Procurement G6', 1),
	('Treaty on the Non-Proliferation of Nuclear Weapons', 1),
	('Asian Infrastructure Investment Bank', 1),
	('Petrocaribe', 1),
	('Forum of East Asia-Latin America Cooperation', 1),
	('Convention on preventing and combating violence against women and domestic violence', 1),
	('International Commission for the Protection of the Rhine', 1),
	('International Lake Constance conference', 1),
	('International Mobile Satellite Organization', 1),
	('IT-Planungsrat', 1),
	('Organization for Cooperation of Railways', 1),
	('IBSA Dialogue Forum', 1),
	('International Telecommunications Satellite Organization', 1),
	('G8+5', 1),
	('g7+', 1),
	('Group of Ten', 1),
	('European Civil Aviation Conference', 1),
	('Euro-Atlantic Partnership Council', 1),
	('Open Government Partnership', 1),
	('Office of the United Nations High Commissioner for Refugees', 1),
	('Digital 9', 1),
	('Q12183902', 1),
	('Association of Caribbean States', 1),
	('United Nations Economic Commission for Africa', 1),
	('Creative Cities Network', 1),
	('International Confederation of Free Trade Unions', 1),
	('CGIAR', 1),
	('Colombo Plan', 1),
	('International Trade Union Confederation', 1),
	('Association Trio', 1),
	('Convention on the Rights of Persons with Disabilities', 1),
	('Paris Charter', 1),
	('Cairns Group', 1),
	('Francophonie', 1),
]