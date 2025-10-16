
let e = entity qid;
    economy = entity e.P8744.id;
    to_list_class = \l ->
      case compare l 5 of {
        LT => "gp-short-list" ;
        _  => case compare l 10 of {
                LT => "gp-medium-list" ;
                _  => "gp-long-list"
              }
      } ;
    is_metric =
      option "" of {
        mkNP aPl_Det (mkCN metric_1_A unit_1_N) => True;
        mkNP aPl_Det (mkCN imperial_2_A unit_1_N) => False
      };
in <div>
     <h1 class="gp-page-title">expr qid</h1>
     
     case is_metric of {True =>""; False =>""};

     -- Infobox with flag, coat of arms and map
     <div class="infobox">
       <table border=1>
         <tr><td><table>
         <tr>
           <td>[concat: 1 | <img src=(e.P41.s) height=78/>]</td>
           <td>[concat: 1 | <img src=(e.P94.s) height=78/>]</td>
         </tr>
         <tr>
           <td>flag_1_N</td>
           <td>coat_of_arms_N</td>
         </tr>
         </table></td></tr>
         <tr><td>[concat: 1 | <img src=(e.P242.s) width=250/>]</td></tr> 
       </table>
     </div>

     <p>
     -- country region and population
     
    -- TODO: countries in several reqions
    let region =
            "Q21195"    -- Scandinavia
          | "Q7204"     -- Middle East
          | "Q27275"    -- Central Asia
          | "Q27394"    -- Southern Africa
          | "Q27407"    -- East Africa
          | "Q27381"    -- North Africa
          | "Q27509"    -- Central Europe
          | "Q27496"    -- Western Europe
          | "Q27468"    -- Eastern Europe
          | "Q27449"    -- Southern Europe
          | "Q18869"    -- Caucasus
          | "Q35942"    -- Polynesia
          | "Q37394"    -- Melanesia
          | "Q3359409"  -- Micronesia
          | "Q664609" ; -- Caribbean
        country_region = e.P361.id | e.P706.id ;

        cn0 = [list: and_Conj | mkCN (expr e.P31.id)] ;
        cn1 = mkCN' [one | case e.P361.id of {
                             "Q52062"  => nordic_2_A ;
                             "Q39731"  => baltic_2_A ;
                             "Q4412"   => west_african_A ;
                             "Q27433"  => central_african_A ;
                             "Q31945"  => arabic_A ;
                             "Q143487" => arabic_A ;
                             "Q779924" => muslim_A ;
                             _         => variants {}
                           }] cn0 ;
        cn2 = mkCN' cn1 [one | let preposition = 
                                     case lang of {
                                       "spa"|"fre" => of_1_Prep ;
                                       _           => in_1_Prep
                                     } ;
                               in case compare country_region region of {
                                    EQ => mkAdv preposition (mkNP (expr region)) ;
                                    _  => case <compare country_region "Q23522",compare "Q43" qid> of {
                                            <_,EQ> => variants {} ;
                                            <EQ,_> => mkAdv on_1_Prep (mkNP (expr e.P706.id)) ;
                                            _      => variants {}
                                          }
                                  } | 
                                  mkAdv preposition [list: and_Conj | <[filter | <mkNP <expr e.P30.id : LN>,[one | case e.P30.P582.time | "X" of {"X" => True; _ => False}]>] : NP>]
                        ] ;
        population = [select: -1 | <mkNP (mkDet (mkDecimal <e.P1082.amount : Predef.Int>)) (mkCN inhabitantMasc_1_N),e.P1082.P585.time>]
    in case lang of {
         "fin" => [concat: 1 | mkPhrMark (mkS (mkCl (mkNP (expr qid)) (mkNP aSg_Det cn2))) ;
                               mkPhrMark (mkS (ExistNPAdv population there_1_Adv))] ;
         _     => [concat: 1 | mkPhrMark (mkS (mkCl (mkNP (expr qid)) (mkVP (mkNP' (mkNP a_Quant cn2) (mkAdv with_Prep population)))))]
       };

    -- neighbours
    [concat: 1 | 
        let prep = case lang of {
                     "rus" => at_2_Prep;
                     "fin" => in_1_Prep;
                     _     => to_2_Prep
                   };
            article = case lang of {
                       "bul" => aSg_Det;
                       _     => the_Det
                      };
            neighbours = [list: and_Conj
                            | mkNP' (mkNP (expr e.P47.id)) (mkAdv prep (mkNP article [one|expr e.P47.P654.id]))];
            num = [len: (\l -> case compare l 1 of {
                                 EQ => aSg_Det ;
                                 _  => aPl_Det
                               })
                            | e.P47.id];
        in case lang of {
             "fin" => mkPhrMark (mkCl (mkNP (mkQuant it_Pron) NumPl abutterMasc_N) neighbours);
             "rus" => mkPhrMark (mkCl (mkNP it_Pron) (mkVP (mkVP border_5_V) (mkAdv with_Prep neighbours)));
             "fre" => mkPhrMark (mkCl (mkNP theSg_Det country_2_N) (mkVP have_1_V2
                                                 (mkNP num (mkCN (mkCN border_1_N) (mkAdv with_Prep neighbours)))));
             "bul" => mkPhrMark (mkCl (mkNP (ProDrop she_Pron)) (mkVP have_1_V2
                                                 (mkNP num (mkCN (mkCN border_1_N) (mkAdv with_Prep neighbours)))));
             "spa" => mkPhrMark (mkCl (mkNP (ProDrop it_Pron)) (mkVP have_1_V2
                                                 (mkNP num (mkCN (mkCN border_1_N) (mkAdv with_Prep neighbours)))));
             _     => mkPhrMark (mkCl (mkNP it_Pron) (mkVP have_1_V2
                                                 (mkNP num (mkCN (mkCN border_1_N) (mkAdv with_Prep neighbours)))))
           }
     ];

     [concat : 1 | 
        let area =
              case is_metric of {
                 True  => mkNP (mkDet (mkDecimal (round e.P2046.amount 2))) (expr "Q712226") ;
                 False => mkNP (mkDet (mkDecimal (round (mulFloat e.P2046.amount 0.3861021585424458) 2))) (expr "Q232291")
              } ;
            copula = case lang of {
                       "fre" => mkVP (mkAdv of_1_Prep area);
                       "rus" => (mkVP amount_to_1_V2 area);
                       _     => mkVP area
                     }
        in mkPhrMark (mkCl (mkNP theSg_Det area_6_N) copula)];
    
     let capitals = [list: and_Conj | mkNP (expr e.P36.id)];
         num = [len: (\l -> case compare l 1 of {
                              EQ => aSg_Det ;
                              _  => aPl_Det
                            })
                     | e.P36.id];
         order = case lang of {
                   "rus" => mkCl capitals (mkNP the_Det capital_3_N);
                   _     => mkCl (mkNP num capital_3_N) capitals
                 }
     in mkPhrMark (mkS order) ;

     -- TODO: exclude official_langs from other_langs
     let official_langs = [list: and_Conj | mkNP (expr e.P37.id)];
         other_langs    = [list: and_Conj | mkNP (expr e.P2936.id)] ;
         num1 = [len: (\l -> case compare l 1 of {
                               EQ => aSg_Det ;
                               _  => aPl_Det
                             })
                    | e.P37.id];
         num2 = [len: (\l -> case compare l 1 of {
                               EQ => aSg_Det ;
                               _  => aPl_Det
                             })
                    | e.P2936.id];
         vp = case lang of {
                "bul" | "cat" | "ita" | "por" | "spa" => reflexiveVP speak_3_V2;
                "rus" => passiveVP spread_8_V2;
                _     => passiveVP speak_3_V2
              }
     in [concat: 1 |
           mkPhrMark
             ( mkS but_1_Conj (mkS (mkCl official_langs (mkNP num1 (mkCN official_1_A (mkCN language_1_N)))))
                              (mkS (mkCl other_langs (mkVP also_AdV vp)))
             | mkS (mkCl (mkNP num1 (mkCN official_1_A (mkCN language_1_N))) official_langs)
             | mkS (mkCl (mkNP num2 (mkCN spoken_A (mkCN language_1_N))) other_langs)
             )] ;
    </p>

    
    <h2 class="gp-page-title">demography_N</h2>
    -- life expectancy 
    let prep = case lang of {
                 "spa" => of_1_Prep ;
                 _     => in_1_Prep
               };
        number = mkNP (mkDecimal (round <e.P2250.amount: Predef.Float> 2)) year_5_N;
        highest = mkNP (mkDet the_Quant NumSg (mkOrd high_1_A)) (mkCN life_expectancy_N);
        lowest = mkNP (mkDet the_Quant NumSg (mkOrd low_1_A)) (mkCN life_expectancy_N);
        average = mkAdv with_Prep (mkNP a_Det (mkCN (mkCN average_1_N (mkAdv of_1_Prep number))));
    in [concat: 1 |
          case qid of {
            "Q238" => mkPhrMark (mkCl (mkNP (expr qid)) (mkVP have_1_V2 (AdvNP highest
                                      (mkAdv prep (AdvNP (mkNP theSg_Det (mkCN world_1_N)) average)))));
            "Q17"  => mkPhrMark (mkCl (mkNP (expr qid)) (mkVP have_1_V2 (AdvNP highest
                                      (mkAdv prep (AdvNP (mkNP asia_1_LN) average)))));
            "Q262" => mkPhrMark (mkCl (mkNP (expr qid)) (mkVP have_1_V2 (AdvNP highest
                                      (mkAdv prep (AdvNP (mkNP africa_LN) average)))));
            "Q16"  => mkPhrMark (mkCl (mkNP (expr qid)) (mkVP have_1_V2 (AdvNP highest
                                      (mkAdv prep (AdvNP (mkNP north_america_1_LN) average)))));
            "Q298" => mkPhrMark (mkCl (mkNP (expr qid)) (mkVP have_1_V2 (AdvNP highest
                                      (mkAdv prep (AdvNP (mkNP south_america_1_LN) average)))));
            "Q408" => mkPhrMark (mkCl (mkNP (expr qid)) (mkVP have_1_V2 (AdvNP highest
                                      (mkAdv prep (AdvNP (mkNP insular_oceania_LN) average)))));
            "Q1044" =>mkPhrMark (mkCl (mkNP (expr qid)) (mkVP have_1_V2 (AdvNP lowest
                                      (mkAdv prep (AdvNP (mkNP theSg_Det (mkCN world_1_N)) average)))));
            "Q212" => mkPhrMark (mkCl (mkNP (expr qid)) (mkVP have_1_V2 (AdvNP lowest
                                      (mkAdv prep (AdvNP (mkNP europe_1_LN) average)))));
            "Q889" => mkPhrMark (mkCl (mkNP (expr qid)) (mkVP have_1_V2 (AdvNP lowest
                                      (mkAdv prep (AdvNP (mkNP asia_1_LN) average)))));
            "Q790" => mkPhrMark (mkCl (mkNP (expr qid)) (mkVP have_1_V2 (AdvNP lowest
                                      (mkAdv prep (AdvNP (mkNP north_america_1_LN) average)))));
            "Q734" => mkPhrMark (mkCl (mkNP (expr qid)) (mkVP have_1_V2 (AdvNP lowest
                                      (mkAdv prep (AdvNP (mkNP south_america_1_LN) average)))));
            "Q709" => mkPhrMark (mkCl (mkNP (expr qid)) (mkVP have_1_V2 (AdvNP lowest
                                      (mkAdv prep (AdvNP (mkNP insular_oceania_LN) average)))));
            _      => mkPhrMark (mkCl (mkNP the_Det life_expectancy_N) number)
          }];

    let np = [select: -1 | <mkNP (mkDecimal (round <e.P4841.amount: Predef.Float> 2)) (mkCN (mkCN child_2_N)), e.P4841.P585.time>]
    in [concat: 1 |
	      mkPhrMark (mkS (mkCl (mkNP theSg_Det fertility_1_N) (mkNP np (mkAdv per_Prep (mkNP woman_1_N)))))];

    let death_case =
          case lang of {
            "eng"|"spa"|"fre" => death_1_N ;
            _                 => CompoundN death_1_N case_1_N
          } ;
        np = mkNP (mkDecimal (round e.P3864.amount 2)) (mkCN death_case)
    in [concat: 1 | 
          mkPhrMark (mkS (mkCl (mkNP the_Det (CompoundN suicide_1_N rate_4_N))
                               (mkVP stand_at_V2 (mkNP np (mkAdv per_Prep (mkNP (mkDecimal 100000) (mkCN inhabitantMasc_1_N yearly_Adv)))))))];
 
    let city = case qid of {
	             "Q668" => <"Q1353", <26495000 : Predef.Int > >;
                 "Q148" => <"Q8686", <24870895 : Predef.Int > >;
                 "Q902" => <"Q1354", <16800000 : Predef.Int > >;
                 "Q43" => <"Q406", <15462452 : Predef.Int > >;
                 "Q1033" => <"Q8673", <15070000 : Predef.Int > >;
                 "Q843" => <"Q8660", <14910352 : Predef.Int > >;
                 "Q17" => <"Q1490", <14047594 : Predef.Int > >;
                 "Q159" => <"Q649", <12455682 : Predef.Int > >;
                 "Q155" => <"Q174", <12325232 : Predef.Int > >;
                 "Q974" => <"Q3838", <11855000 : Predef.Int > >;
                 "Q252" => <"Q3630", <10562088 : Predef.Int > >;
                 "Q881" => <"Q1854", <10380000 : Predef.Int > >;
                 "Q419" => <"Q2868", <9943800 : Predef.Int > >;
                 "Q503585" => <"Q8684", <9668465 : Predef.Int>>;
                 "Q884" => <"Q8684", <9668465 : Predef.Int>>;
                 "Q79" => <"Q85", <9606916 : Predef.Int>>;
                 "Q96" => <"Q1489", <9209944 : Predef.Int>>;
                 "Q145" => <"Q84", <8908081 : Predef.Int>>;
                 "Q30" => <"Q60", <8804190 : Predef.Int>>;
                 "Q794" => <"Q3616", <8693706 : Predef.Int>>;
                 "Q851" => <"Q3692", <8002100 : Predef.Int>>;
                 "Q1065073" => <"Q404817", <7816831 : Predef.Int>>;
                 "Q739" => <"Q2841", <7743955 : Predef.Int>>;
                 "Q836" => <"Q37995", <7360703 : Predef.Int>>;
                 "Q796" => <"Q1530", <6960000 : Predef.Int>>;
                 "Q8733" => <"Q144663", <6645243 : Predef.Int>>;
                 "Q298" => <"Q2887", <6257516 : Predef.Int>>;
                 "Q334" => <"Q334", <5866139 : Predef.Int>>;
                 "Q869" => <"Q1861", <5676648 : Predef.Int>>;
                 "Q114" => <"Q3870", <5545000 : Predef.Int>>;
                 "Q1049" => <"Q1963", <5345000 : Predef.Int>>;
                 "Q1008" => <"Q1515", <4980000 : Predef.Int>>;
                 "Q408" => <"Q3130", <4840600 : Predef.Int>>;
                 "Q924" => <"Q1960", <4715000 : Predef.Int>>;
                 "Q258" => <"Q34647", <4434827 : Predef.Int>>;
                 "Q865" => <"Q244898", <4364124 : Predef.Int>>;
                 "Q889" => <"Q5838", <4273156 : Predef.Int>>;
                 "Q810" => <"Q3805", <4007526 : Predef.Int>>;
                 "Q183" => <"Q64", <3677472 : Predef.Int>>;
                 "Q1028" => <"Q7903", <3499000 : Predef.Int>>;
                 "Q262" => <"Q3561", <3415811 : Predef.Int>>;
                 "Q878" => <"Q612", <3331420 : Predef.Int>>;
                 "Q750" => <"Q170688", <3151676 : Predef.Int>>;
                 "Q414" => <"Q1486", <3120612 : Predef.Int>>;
                 "Q115" => <"Q3624", <3041002 : Predef.Int>>;
                 "Q817" => <"Q35178", <2989000 : Predef.Int>>;
                 "Q928" => <"Q1475", <2960048 : Predef.Int>>;
                 "Q805" => <"Q2471", <2957000 : Predef.Int>>;
                 "Q212" => <"Q1899", <2952301 : Predef.Int>>;
                 "Q38" => <"Q220", <2872800 : Predef.Int>>;
                 "Q423" => <"Q18808", <2863000 : Predef.Int>>;
                 "Q16" => <"Q172", <2794356 : Predef.Int>>;
                 "Q1009" => <"Q132830", <2768436 : Predef.Int>>;
                 "Q736" => <"Q43509", <2723665 : Predef.Int>>;
                 "Q265" => <"Q269", <2571668 : Predef.Int>>;
                 "Q858" => <"Q3766", <2503000 : Predef.Int>>;
                 "Q241" => <"Q1563", <2492618 : Predef.Int>>;
                 "Q916" => <"Q3897", <2487444 : Predef.Int>>;
                 "Q953" => <"Q3881", <2467563 : Predef.Int>>;
                 "Q965" => <"Q3777", <2453496 : Predef.Int>>;
                 "Q822" => <"Q3820", <2421354 : Predef.Int>>;
                 "Q117" => <"Q3761", <2388000 : Predef.Int>>;
                 "Q227" => <"Q9248", <2300500 : Predef.Int>>; 
                 "Q717" => <"Q1533", <2245744 : Predef.Int>>; 
                 "Q945" => <"Q3792", <2188376 : Predef.Int>>;
                 "Q954" => <"Q3921", <2150000 : Predef.Int>>;
                 "Q142" => <"Q90", <2145906 : Predef.Int>>;
                 "Q424" => <"Q1850", <2129371 : Predef.Int>>;
                 "Q1045" => <"Q2449", <2120000 : Predef.Int>>;
                 "Q912" => <"Q3703", <2009109 : Predef.Int>>;
                 "Q184" => <"Q2280", <1995471 : Predef.Int>>;
                 "Q2415901" => <"Q56036", <1984837 : Predef.Int>>;
                 "Q833" => <"Q1865", <1982100 : Predef.Int>>;
                 "Q40" => <"Q1741", <1973403 : Predef.Int>>;
                 "Q232" => <"Q35493", <1916822 : Predef.Int>>;
                 "Q1020" => <"Q188693", <1895973 : Predef.Int>>;
                 "Q36" => <"Q270", <1860281 : Predef.Int>>;
                 "Q971" => <"Q3844", <1827000 : Predef.Int>>;
                 "Q218" => <"Q19660", <1716983 : Predef.Int>>;
                 "Q28" => <"Q1781", <1706851 : Predef.Int>>;
                 "Q783" => <"Q3238", <1682725 : Predef.Int>>;
                 "Q1036" => <"Q3894", <1680600 : Predef.Int>>;
                 "Q1006" => <"Q3733", <1667864 : Predef.Int>>;
                 "Q403" => <"Q2074197", <1659440 : Predef.Int>>;
                 "Q664" => <"Q37100", <1470100 : Predef.Int>>;
                 "Q1041" => <"Q3718", <1438725 : Predef.Int>>;
                 "Q842" => <"Q3826", <1421409 : Predef.Int>>;
                 "Q711" => <"Q23430", <1396288 : Predef.Int>>;
                 "Q219" => <"Q472", <1383435 : Predef.Int>>;
                 "Q213" => <"Q1085", <1357326 : Predef.Int>>;
                 "Q786" => <"Q42763", <1343423 : Predef.Int>>;
                 "Q77" => <"Q1335", <1319108 : Predef.Int>>;
                 "Q1016" => <"Q3579", <1293016 : Predef.Int>>;
                 "Q16957" => <"Q56037", <1279212 : Predef.Int>>;
                 "Q1019" => <"Q3915", <1275207 : Predef.Int>>;
                 "Q31" => <"Q240", <1218255 : Predef.Int>>;
                 "Q774" => <"Q1555", <1213651 : Predef.Int>>;
                 "Q1029" => <"Q3889", <1191613 : Predef.Int>>;
                 "Q846" => <"Q3861", <1186023 : Predef.Int>>;
                 "Q1037" => <"Q3859", <1156663 : Predef.Int>>;
                 "Q813" => <"Q9361", <1120827 : Predef.Int>>;
                 "Q230" => <"Q994", <1118035 : Predef.Int>>;
                 "Q657" => <"Q3659", <1092066 : Predef.Int>>;
                 "Q1025" => <"Q3688", <1077169 : Predef.Int>>;
                 "Q399" => <"Q1953", <1075800 : Predef.Int>>;
                 "Q33296" => <"Q158467", <1069276 : Predef.Int>>;
                 "Q1032" => <"Q3674", <1026848 : Predef.Int>>;
                 "Q1014" => <"Q3748", <1021762 : Predef.Int>>;
                 "Q790" => <"Q34261", <987310 : Predef.Int>>;
                 "Q34" => <"Q1754", <978770 : Predef.Int>>;
                 "Q986" => <"Q3642", <963000 : Predef.Int>>;
                 "Q1044" => <"Q3780", <951000 : Predef.Int>>;
                 "Q811" => <"Q3274", <937489 : Predef.Int>>;
                 "Q55" => <"Q727", <921468 : Predef.Int>>;
                 "Q801" => <"Q1218", <919438 : Predef.Int>>;
                 "Q797422" => <"Q223761", <903887 : Predef.Int>>;
                 "Q797440" => <"Q223761", <903887 : Predef.Int>>;
                 "Q929" => <"Q3832", <889231 : Predef.Int>>;
                 "Q804" => <"Q3306", <880691 : Predef.Int>>;
                 "Q863" => <"Q9365", <863400 : Predef.Int>>;
                 "Q837" => <"Q3037", <845767 : Predef.Int>>;
                 "Q874" => <"Q23438", <828100 : Predef.Int>>;
                 "Q1000" => <"Q3825", <797003 : Predef.Int>>;
                 "Q1747689" => <"Q131301", <775404 : Predef.Int>>;
                 "Q224" => <"Q1435", <767131 : Predef.Int>>;
                 "Q34754" => <"Q168652", <760000 : Predef.Int>>;
                 "Q854" => <"Q35381", <752993 : Predef.Int>>;
                 "Q20" => <"Q585", <709037 : Predef.Int>>;
                 "Q962" => <"Q43595", <679012 : Predef.Int>>;
                 "Q175276" => <"Q31926034", <666880 : Predef.Int>>;
                 "Q199442" => <"Q31926034", <666880 : Predef.Int>>;
                 "Q29" => <"Q31926034", <666880 : Predef.Int>>;
                 "Q33" => <"Q1757", <664921 : Predef.Int>>;
                 "Q41" => <"Q1524", <664046 : Predef.Int>>;
                 "Q967" => <"Q3854", <658859 : Predef.Int>>;
                 "Q217169" => <"Q193250", <653337 : Predef.Int>>;
                 "Q750583" => <"Q193250", <653337 : Predef.Int>>;
                 "Q890120" => <"Q193250", <653337 : Predef.Int>>;
                 "Q35" => <"Q1748", <644431 : Predef.Int>>;
                 "Q217" => <"Q21197", <639000 : Predef.Int>>;
                 "Q211" => <"Q1773", <605802 : Predef.Int>>;
                 "Q977" => <"Q3604", <603900 : Predef.Int>>;
                 "Q948" => <"Q3572", <602560 : Predef.Int>>;
                 "Q37" => <"Q216", <581475 : Predef.Int>>;
                 "Q766" => <"Q34692", <580000 : Predef.Int>>;
                 "Q27" => <"Q1761", <553165 : Predef.Int>>;
                 "Q45" => <"Q597", <545923 : Predef.Int>>;
                 "Q221" => <"Q384", <526502 : Predef.Int>>;
                 "Q958" => <"Q1947", <525953 : Predef.Int>>;
                 "Q733" => <"Q2933", <524190 : Predef.Int>>;
                 "Q1013" => <"Q3909", <519186 : Predef.Int>>;
                 "Q219060" => <"Q47492", <515556 : Predef.Int>>;
                 "Q1007" => <"Q3739", <492004 : Predef.Int>>;
                 "Q1121819" => <"Q148062", <481300 : Predef.Int>>;
                 "Q214" => <"Q1780", <475503 : Predef.Int>>;
                 "Q129286" => <"Q200340", <451100 : Predef.Int>>;
                 "Q191" => <"Q1770", <438341 : Predef.Int>>;
                 "Q39" => <"Q72", <436332 : Predef.Int>>;
                 "Q1030" => <"Q3935", <431000 : Predef.Int>>;
                 "Q222" => <"Q19689", <418495 : Predef.Int>>;
                 "Q1183" => <"Q41211", <342259 : Predef.Int>>;
                 "Q800" => <"Q3070", <342188 : Predef.Int>>;
                 "Q23681" => <"Q3856", <330000 : Predef.Int>>;
                 "Q229" => <"Q3856", <330000 : Predef.Int>>;
                 "Q691" => <"Q36526", <317374 : Predef.Int>>;
                 "Q792" => <"Q3110", <316090 : Predef.Int>>;
                 "Q124943" => <"Q893274", <315351 : Predef.Int>>;
                 "Q983" => <"Q3818", <297000 : Predef.Int>>;
                 "Q207272" => <"Q588", <285711 : Predef.Int>>;
                 "Q211274" => <"Q588", <285711 : Predef.Int>>;
                 "Q38872" => <"Q588", <285711 : Predef.Int>>;
                 "Q215" => <"Q437", <284293 : Predef.Int>>;
                 "Q225" => <"Q11194", <275524 : Predef.Int>>;
                 "Q778" => <"Q2467", <274400 : Predef.Int>>;
                 "Q12560" => <"Q188894", <266784 : Predef.Int>>;
                 "Q179876" => <"Q128147", <260200 : Predef.Int>>;
                 "Q963" => <"Q3919", <246325 : Predef.Int>>;
                 "Q730" => <"Q3001", <223757 : Predef.Int>>;
                 "Q574" => <"Q9310", <222323 : Predef.Int>>;
                 "Q40362" => <"Q47837", <217732 : Predef.Int>>;
                 "Q734" => <"Q10717", <200500 : Predef.Int>>;
                 "Q1246" => <"Q25270", <198897 : Predef.Int>>;
                 "Q193714" => <"Q192213", <194300 : Predef.Int>>;
                 "Q15180" => <"Q1001104", <185082 : Predef.Int>>;
                 "Q34266" => <"Q1001104", <185082 : Predef.Int>>;
                 "Q1011" => <"Q3751", <159050 : Predef.Int>>;
                 "Q398" => <"Q3882", <157474 : Predef.Int>>;
                 "Q236" => <"Q23564", <150977 : Predef.Int>>;
                 "Q25279" => <"Q132679", <150000 : Predef.Int>>;
                 "Q1027" => <"Q3929", <149194 : Predef.Int>>;
                 "Q189" => <"Q1764", <135688 : Predef.Int>>;
                 "Q907112" => <"Q132572", <133807 : Predef.Int>>;
                 "Q826" => <"Q9347", <133019 : Predef.Int>>;
                 "Q32" => <"Q1842", <132780 : Predef.Int>>;
                 "Q4224856" => <"Q926426", <130495 : Predef.Int>>;
                 "Q819" => <"Q750443", <124000 : Predef.Int>>;
                 "Q870055" => <"Q383622", <119848 : Predef.Int>>;
                 "Q1320058" => <"Q383622", <119848 : Predef.Int>>;
                 "Q28513" => <"Q174684", <110979 : Predef.Int>>;
                 "Q1050" => <"Q495730", <110508 : Predef.Int>>;
                 "Q244" => <"Q36168", <110000 : Predef.Int>>;
                 "Q6250" => <"Q345204", <106277 : Predef.Int>>;
                 "Q712" => <"Q38807", <88271 : Predef.Int>>;
                 "Q685" => <"Q40921", <84520 : Predef.Int>>;
                 "Q754" => <"Q1444575", <83489 : Predef.Int>>;
                 "Q121932" => <"Q185289", <81308 : Predef.Int>>;
                 "Q147909" => <"Q185289", <81308 : Predef.Int>>;
                 "Q815731" => <"Q185289", <81308 : Predef.Int>>;
                 "Q917" => <"Q9270", <79185 : Predef.Int>>;
                 "Q970" => <"Q3901", <74749 : Predef.Int>>;
                 "Q1039" => <"Q3932", <71868 : Predef.Int>>;
                 "Q878818" => <"Q83531", <71501 : Predef.Int>>;
                 "Q760" => <"Q41699", <70000 : Predef.Int>>;
                 "Q172579" => <"Q3476", <69439 : Predef.Int>>;
                 "Q139319" => <"Q40811", <64441 : Predef.Int>>;
                 "Q154667" => <"Q40811", <64441 : Predef.Int>>;
                 "Q245160" => <"Q40811", <64441 : Predef.Int>>;
                 "Q307041" => <"Q40811", <64441 : Predef.Int>>;
                 "Q325493" => <"Q40811", <64441 : Predef.Int>>;
                 "Q330756" => <"Q40811", <64441 : Predef.Int>>;
                 "Q545205" => <"Q40811", <64441 : Predef.Int>>;
                 "Q1069959" => <"Q40811", <64441 : Predef.Int>>;
                 "Q55659450" => <"Q40811", <64441 : Predef.Int>>;
                 "Q12544" => <"Q40811", <64441 : Predef.Int>>;
                 "Q710" => <"Q131233", <63439 : Predef.Int>>;
                 "Q80702" => <"Q187807", <58367 : Predef.Int>>;
                 "Q242" => <"Q108223", <57169 : Predef.Int>>;
                 "Q689837" => <"Q842810", <57035 : Predef.Int>>;
                 "Q133356" => <"Q216363", <56988 : Predef.Int>>;
                 "Q172107" => <"Q216363", <56988 : Predef.Int>>;
                 "Q203493" => <"Q216363", <56988 : Predef.Int>>;
                 "Q243610" => <"Q216363", <56988 : Predef.Int>>;
                 "Q1508143" => <"Q216363", <56988 : Predef.Int>>;
                 "Q2305208" => <"Q216363", <56988 : Predef.Int>>;
                 "Q686" => <"Q37806", <51437 : Predef.Int>>;
                 "Q921" => <"Q9279", <50000 : Predef.Int>>;
                 "Q244165" => <"Q129352", <49848 : Predef.Int>>;
                 "Q70972" => <"Q95895695", <48500 : Predef.Int>>;
                 "Q12548" => <"Q95895695", <48500 : Predef.Int>>;
                 "Q541455" => <"Q571215", <43337 : Predef.Int>>;
                 "Q323904" => <"Q214681", <40017 : Predef.Int>>;
                 "Q683" => <"Q36260", <37708 : Predef.Int>>;
                 "Q21203" => <"Q131243", <34980 : Predef.Int>>;
                 "Q1410" => <"Q1410", <34003 : Predef.Int>>;
                 "Q785" => <"Q147738", <33522 : Predef.Int>>;
                 "Q1005" => <"Q3726", <31356 : Predef.Int>>;
                 "Q23427" => <"Q79863", <30432 : Predef.Int>>;
                 "Q208169" => <"Q208169", <30000 : Predef.Int>>;
                 "Q709" => <"Q12919", <30000 : Predef.Int>>;
                 "Q5785" => <"Q172996", <27704 : Predef.Int>>;
                 "Q1042" => <"Q3940", <26450 : Predef.Int>>;
                 "Q781" => <"Q36262", <24451 : Predef.Int>>;
                 "Q233" => <"Q39583", <24356 : Predef.Int>>;
                 "Q678" => <"Q38834", <23221 : Predef.Int>>;
                 "Q228" => <"Q1863", <22151 : Predef.Int>>;
                 "Q407199" => <"Q1899332", <19197 : Predef.Int>>;
                 "Q223" => <"Q226", <18326 : Predef.Int>>;
                 "Q682001" => <"Q1001326", <17394 : Predef.Int>>;
                 "Q7318" => <"Q1001326", <17394 : Predef.Int>>;
                 "Q27306" => <"Q1001326", <17394 : Predef.Int>>;
                 "Q41304" => <"Q1001326", <17394 : Predef.Int>>;
                 "Q43287" => <"Q1001326", <17394 : Predef.Int>>;
                 "Q784" => <"Q36281", <16582 : Predef.Int>>;
                 "Q757" => <"Q41474", <16532 : Predef.Int>>;
                 "Q964024" => <"Q2078085", <14931 : Predef.Int>>;
                 "Q10957559" => <"Q2078085", <14931 : Predef.Int>>;
                 "Q11703" => <"Q51681", <14477 : Predef.Int>>;
                 "Q1206012" => <"Q640493", <13951 : Predef.Int>>;
                 "Q131964" => <"Q837170", <13278 : Predef.Int>>;
                 "Q153136" => <"Q837170", <13278 : Predef.Int>>;
                 "Q763" => <"Q41295", <13220 : Predef.Int>>;
                 "Q695" => <"Q527748", <8744 : Predef.Int>>;
                 "Q435583" => <"Q3456410", <7956 : Predef.Int>>;
                 "Q31354462" => <"Q236673", <7449 : Predef.Int>>;
                 "Q702" => <"Q42751", <6227 : Predef.Int>>;
                 "Q672" => <"Q34126", <6025 : Predef.Int>>;
                 "Q347" => <"Q1844", <5668 : Predef.Int>>;
                 "Q769" => <"Q41547", <4315 : Predef.Int>>;
                 "Q2914461" => <"Q211318", <4107 : Predef.Int>>;
                 "Q238" => <"Q1848", <4040 : Predef.Int>>;
                 "Q23635" => <"Q30985", <3686 : Predef.Int>>;
                 "Q459780" => <"Q1722578", <2547 : Predef.Int>>;
                 "Q25230" => <"Q993064", <2000 : Predef.Int>>;
                 "Q3113481" => <"Q1411798", <1524 : Predef.Int>>;
                 "Q26273" => <"Q30958", <1338 : Predef.Int>>;
                 "Q2071857" => <"Q429059", <1190 : Predef.Int>>;
                 "Q2571688" => <"Q429059", <1190 : Predef.Int>>;
                 "Q2685298" => <"Q939009", <1183 : Predef.Int>>;
                 "Q25228" => <"Q30994", <1067 : Predef.Int>>;
                 "Q697" => <"Q31026", <747 : Predef.Int>>;
                 "Q192184" => <"Q30970", <714 : Predef.Int>>;
                 "Q36823" => <"Q642787", <541 : Predef.Int>>;
                 "Q237" => <"Q237", <453 : Predef.Int>>;
                 "Q154195" => <"Q998529", <361 : Predef.Int>>;
                 "Q13353" => <"Q30990", <0 : Predef.Int > >
               };
        prep = case lang of {
    	         "spa" | "fre" => of_1_Prep; 
                 _ => in_1_Prep 
   	           }
    in [concat: 1 | mkPhrMark (mkCl (mkNP (expr city.p1))
                                    (mkNP (mkNP (mkNP (mkDet the_Quant NumSg (mkOrd large_1_A)) (mkCN city_1_N)) (mkAdv prep (mkNP (expr qid)))) 
                                          (mkAdv with_Prep (mkNP (mkDecimal city.p2) inhabitantMasc_1_N))))];
 
    [select: -1 | let hdi = e.P1081.amount ;
                      high = case lang of {
                               "fre" => grand_5_A ;
                               _     => high_1_A
                             } ;
                      low  = case lang of {
                               "fre" => weak_9_A ;
                               _     => low_1_A
                             } ;
                      ap = case compare hdi 0.8 of {
                             LT => case compare hdi 0.7 of {
                                     LT => case compare hdi 0.550 of {
                                             LT => mkAP low ;
                                             _  => mkAP medium_1_A
                                           } ;
                                     _  => mkAP high
                                   } ;
                             _  => mkAP very_AdA high
                           } ;
                      quality = mkCN ap (mkCN human_development_N) ;
                      html = <span>
                            mkPhr (mkUtt (mkCl (mkNP theSg_Det country_1_N) (mkVP have_1_V2 (mkNP aSg_Det quality))));
                            "("; hdi_PN; hdi; ")"; FullStop
                            </span>
                  in <html, e.P1081.P585.time>];
 
    -- TODO: show separately for man an woman
    let prep = case lang of {
	             "spa" | "fre" => in_2_Prep;
                 "rus" => at_7_Prep; 
                 _ => at_1_Prep
               }
    in [concat : 1 | 
          mkPhrMark (mkS (mkCl (mkNP (expr qid))
                               (mkVP establish_2_V2 (mkNP (mkNP theSg_Det (mkCN age_of_majority_N)) 
                                                          (mkAdv prep (mkNP (mkDecimal (round <e.P2997.amount : Predef.Float> 2)) year_5_N))))))];

	-- TODO: show separately for man an woman
    let number = mkNP (mkDecimal (round <e.P3000.amount : Predef.Float> 2)) year_5_N;
        copula = case lang of {
                   "fre" => mkVP (mkAdv of_1_Prep number);
                   "rus" => mkVP amount_to_1_V2 number; 
                   _     => mkVP number
                 }
    in [concat : 1 | 
  	       mkPhrMark (mkS (mkCl (mkNP (mkNP the_Det (mkCN minimum_A age_1_N)) (mkAdv of_3_Prep (mkNP marriage_1_N))) 
  	                            copula))
       ];

  	-- TODO: show separately for man an woman
    let number = mkNP (mkDecimal (round <e.P3001.amount : Predef.Float> 2)) year_5_N;
        copula = case lang of {
                   "fre" => mkVP (mkAdv of_1_Prep number);
                   "rus" => mkVP amount_to_1_V2 number; 
                   _     => mkVP number
                 }
    in [concat : 1 | 
           mkPhrMark (mkS (mkCl (mkNP (mkNP the_Det (mkCN age_1_N)) (mkAdv of_3_Prep (mkNP retirement_1_N))) 
                                copula))];

    -- TODO: laicism
    [concat: 1 | 
        let faith_expr = \qid ->
              case qid of {
                "Q752470" => mkNP (mkCN eastern_4_A (mkCN orthodox_3_A christianity_1_N)) ; -- Finnish Orthodox Church --> Eastern Orthodox Christianity
                "Q9592"   => mkNP catholicism_N ;
                "Q163943" => mkNP druzism_N ;
                "Q728697" => mkNP (mkCN secular_3_A state_4_N) ;
                "Q1379849"=> mkNP lutheranism_N ; -- Evangelical Lutheran Church of Finland --> Lutheranism
                _         => mkNP (expr qid)
              } ;
            religions = [list: and_Conj | <faith_expr e.P3075.id : NP>] ;
            num = [len: (\l -> case compare l 1 of {
                                 EQ => theSg_Det ;
                                 _  => thePl_Det
                               })
                            | e.P3075.id];
        in mkPhrMark (mkS (mkCl (mkNP num (mkCN official_3_A religion_2_N)) religions))];

   <h2 class="gp-page-title">education_2_N</h2>
   -- obligatory education
   let prep = case lang of {
   	            "spa" => out_of_2_Prep;
                "fre" => as_of_Prep;
                _     => from_Prep
              };
       article = case lang of {
   	               "spa" | "fre" => thePl_Det; 
                   _             => aPl_Det
                 };
       number = QuantityNP (mkDecimal (round e.P6897.amount 2)) percent_MU;
       copula = case lang of {
                  "fre" => mkVP (mkAdv of_1_Prep number);
                  "rus" => (mkVP amount_to_1_V2 number); 
                  _     => mkVP number
                };
       from = mkAdv from_Prep (mkNP (mkDecimal (round e.P3270.amount 2)) year_5_N) ;
       to   = mkAdv to_1_Prep (mkNP (mkDecimal (round e.P3271.amount 2)) year_5_N) ;
       phr1 = mkPhrMark (mkCl (mkNP education_2_N)
                              (mkAP (mkAP obligatory_1_A)
                                    (mkAdv for_Prep 
                                           (mkNP article (mkCN (mkCN (mkCN child_1_N) from) to
                                                         |      mkCN (mkCN child_1_N) from
                                                         |mkCN       (mkCN child_1_N)       to
                                                         ))))) ;
       phr2 = mkPhrMark (mkCl this_NP (mkVP result_in_V2 (mkNP (mkNP aSg_Det literacy_rate_N) (mkAdv of_1_Prep number)))) ;
       phr3 = mkPhrMark (mkCl (mkNP theSg_Det literacy_rate_N) copula) ;
       p1 = <p>phr1; phr2</p>
       p2 = <p>phr1</p>
       p3 = <p>phr3</p>
   in [one | p1 | p2 | p3];

   [concat: 1 | mkPhrMark (mkCl (mkNP (mkDecimal (round e.P2573.amount 2)) child_1_N)
                                (mkAdv out_of_3_Prep (mkNP theSg_Det education_system_N)))];

   [concat: 1 | let prOut = round (mulFloat (divFloat e.P2573.amount (int2float e.P1082.amount)) 100.0) 2
                in mkPhrMark (mkCl this_NP 
                                   (mkVP amount_to_1_V2
                                         (mkNP (QuantityNP (mkDecimal prOut) percent_MU)
    	                                       (mkAdv of_1_Prep (mkNP theSg_Det population_1_N)))))];

    <h2 class="gp-page-title">mkNP aPl_Det (mkCN administrative_A unit_3_N)</h2>

    -- not a dot but a semicolumn
    [concat: 1 | mkPhr (mkCl (mkNP theSg_Det country_1_N)
                             (mkVP have_1_V2 (mkNP thePl_Det 
                                                   (mkCN following_2_A (mkCN administrative_A unit_3_N))))); ":"];

    <ul class=[len: to_list_class | e.P150]>[concat | <li>expr e.P150.id</li>]</ul>


    <h2 class="gp-page-title">politics_5_N</h2>

    let basicForm = entity e.P122.id;
        name = [select: -1 | <expr {NP} e.P35.id, e.P35.P580.time>];
        position1 = case e.P1906.id of {
                      "Q844944" => mkCN chairman_N (mkAdv of_1_Prep (mkNP the_Det presidency_2_N));
                      "Q955006" | "Q191954" => mkCN presidentMasc_1_N;
                      "Q25711499" => mkCN emir_N;
                      "Q63415597" | "Q2457774" => mkCN prince_N;
                      "Q258045" => mkCN (CompoundN captainMasc_1_N regentMasc_1_N);
                      "Q2081829" => mkCN amir_N ;
                      "Q1402561" => mkCN (mkCN military_2_A leaderMasc_1_N);
                      "Q1472951" =>  mkCN governor_generalMasc_N;
                      "Q102181806" => mkCN chairman_N (mkAdv of_1_Prep (mkNP the_Det (mkCN presidential_1_A council_1_N)));
                      "Q63107773" => mkCN chairman_N (mkAdv of_1_Prep
                                                                 (mkNP the_Det (mkCN transitional_A (mkCN military_2_A council_1_N))));
                      _ => mkCN (expr e.P1906.id)
                    };
        position2 = case e.P1906.P279.id of {
                      "Q15995642" | "Q611644" => mkCN pope_1_N;
                      "Q30461" | "Q248577" => mkCN presidentMasc_1_N;
                      "Q43292" =>  mkCN sultan_N;
                      "Q7645115" => mkCN supreme_2_A leaderMasc_1_N;
                      "Q166382" => mkCN emir_N;
                      "Q39018" => mkCN emperor_1_N;
                      "Q116" | "Q12097" | "Q16511993" => mkCN monarchMasc_1_N;
                      _ => expr e.P1906.P279.id
                    }
    in [concat: 1 | mkPhrMark (mkCl (mkNP (expr qid))
                                    (mkNP aSg_Det
                                          (mkCN' (expr basicForm.P279.id)
	                                             (mkAdv with_Prep 
                                                        (mkNP (mkNP (mkCN position1 name) | mkNP (mkCN position2 name) | name)
                                                              (mkAdv as_Prep (mkNP head_of_stateMasc_N)))))))
       ];

    -- TODO: family relation?
    let prev_head = [select: -2 | <expr e.P35.id, e.P35.P580.time>];
        pron      = [select: -1 |
                       let pron = case (entity e.P35.id).P21.id of {
                                    "Q6581097" => he_Pron;
                                    _          => she_Pron
                                  }
                       in <pron, e.P35.P580.time>];
        prep = case lang of {
                 "fre" => into_1_Prep;
                 _ => in_1_Prep
               }
    in [concat: 1 | mkPhrMark (mkS TPastSimple 
                                   (mkCl (mkNP pron)
                                         (mkVP (mkVP succeed_V2 prev_head)
                                               (mkAdv prep (mkNP the_Det position_6_N)))))];

    -- TODO: family relation?
    let officeGov = entity e.P1313.id ;
        name      = [select: -1 | <expr e.P6.id, e.P6.P580.time>];
        prev_name = [select: -2 | <expr e.P6.id, e.P6.P580.time>]
    in [concat: 1 | mkPhrMark (mkCl (mkNP the_Det (mkCN current_A head_of_government_N))
                                    ( ExtRelNP (mkNP (mkCN (expr officeGov.P279.id) name))
                                               (mkRS TPastSimple (mkRCl which_RP (mkVP (mkVP take_office_V)
                                                                                       (mkAdv after_Prep prev_name))))
                                    | mkNP (mkCN (expr officeGov.P279.id) name)
                                    | name
                                    ))] ;

    [concat: 1 | let orgs = [list: and_Conj | mkNP (expr e.P463.id)]
                 in mkPhrMark (mkCl (mkNP theSg_Det country_1_N) (mkNP aSg_Det (PossNP (mkCN member_4_N) orgs)))];

    let number = <e.P8328.amount : Predef.Float>;
        democracy = case compare number 9.0 of {
                      LT => case compare number 6.0 of {
                              LT => case compare number 4.0 of {
                                      LT => mkNP a_Quant (mkCN authoritarian_1_A regime_1_N);
                                      _  => mkNP a_Quant (mkCN hybrid_A regime_1_N)
                                    };
                              _  => case lang of {
                                      "fre" | "spa" => mkNP a_Quant (mkCN imperfect_1_A democracy_2_N);
                                      _             => mkNP a_Quant (mkCN democracy_2_N (mkAdv with_Prep (mkNP aPl_Det flaw_3_N)))
                                    }
                            };
                      _  => case lang of {
                              "fre" => mkNP a_Quant (mkCN full_fledged_1_A democracy_2_N) ;
                              _     => mkNP a_Quant (mkCN full_2_A democracy_2_N)
                            }
                    };
        vp = case lang of {
               "rus" => passiveVP (Slash3V3 consider_6_V3 democracy);
               _     => mkVP (passiveVP (mkVPSlash rank_2_V2)) (mkAdv as_Prep democracy)
             }
    in [concat: 1 | mkPhrMark (ExtAdvS
                                  (mkAdv with_Prep (mkNP (mkNP a_Quant democracy_index_N)
                                                         (mkAdv of_1_Prep (mkNP (mkDecimal number) point_10_N))))
                                  (mkS (mkCl (mkNP (expr qid))
                                             (mkVP (passiveVP (mkVPSlash rank_2_V2)) (mkAdv as_Prep democracy)))))];

    let freedom = entity e.P1552.id ;
        quality = case freedom.P3729.id of {
                    "Q3174312" | "Q47185282" => mkNP aSg_Det (mkCN free_1_A country_1_N);
                    "Q47185145" => mkNP aSg_Det (mkCN (mkAP partly_AdA free_1_A) country_1_N);
                    "Q7174" => mkNP aSg_Det (mkCN democratic_1_A country_1_N)
                  };
        pol = case freedom.P3729.id of {
                "Q47185282" => PNeg;
                _           => PPos
              }
    in [concat:1 | mkPhrMark (mkS pol (mkCl (mkNP freedom_in_the_world_PN)
                                            (mkVP (mkVPSlash consider_6_V3 (mkNP it_Pron)) quality)))];

    let agents = [list: and_Conj | mkNP (expr e.P3461.id)]
    in [concat: 1 | mkPhrMark (mkCl (mkNP (ProDrop it_Pron))
  	                                (PassAgentVPSlash (AdvVPSlash (mkVPSlash designate_4_V2)
                                                                  (mkAdv as_Prep (mkNP aSg_Det (CompoundN terroristMasc_N state_4_N))))
                                                      agents))];

    <h2 class="gp-page-title">economy_1_N</h2>
    -- fix growth
    
    let gdp0 = QuantityNP (mkDecimal (round economy.P2131.amount 2)) dollar_MU ;
        gdp  = [default: gdp0 | mkNP and_Conj gdp0
		                             (mkNP (QuantityNP (mkDecimal (round economy.P2132.amount 2)) dollar_MU) per_capita_Adv)];
        growth = case compare economy.P2219.amount 0.0 of {
    	           GT => growth_3_N;
                   _  => decline_1_N
                 };
	    number = mkNP' (mkNP gdp) (mkAdv with_Prep 
                                         (mkNP (mkNP aSg_Det growth)
                                               (mkAdv of_1_Prep (QuantityNP (mkDecimal (round economy.P2219.amount 2)) percent_MU))));
	    copula = case lang of {
                   "fre" => mkVP (mkAdv of_1_Prep number);
                   "rus" => mkVP amount_to_1_V2 number;
                   _     => mkVP number
                 }
    in [concat : 1 | mkPhrMark (mkCl (mkNP theSg_Det gross_domestic_product_N) copula)];

    -- gdp 
    let number = (QuantityNP (mkDecimal (round economy.P1279.amount 2)) percent_MU);
        copula = case lang of {
                   "fre" => mkVP (mkAdv of_1_Prep number);
                   "rus" => (mkVP amount_to_1_V2 number);
                   _ => mkVP number
                 }
    in [concat: 1 | mkPhrMark (mkCl (mkNP theSg_Det (CompoundN inflation_1_N rate_4_N)) copula)];
    
    [concat: 1 | mkPhrMark (mkCl (mkNP theSg_Det country_2_N)
                           (mkVP have_1_V2 (AdvNP (mkNP aSg_Det (mkCN total_1_A reserve_2_N))
                                                  (mkAdv of_1_Prep (QuantityNP (mkDecimal (round economy.P2134.amount 2)) dollar_MU)))))];

	let income = QuantityNP (mkDecimal (round economy.P3529.amount 2)) dollar_MU;
        number = e.P1125.amount;
        gini = case compare number 50.0 of {
                 GT => <mkCN extreme_1_A inequality_N, but_1_Conj>;
                 _  => case compare number 45.0 of {
                         GT => <mkCN (mkAP very_AdA high_1_A) inequality_N, but_1_Conj>;
                         _  => case compare number 40.0 of {
                                 GT => <mkCN high_1_A inequality_N, but_1_Conj>;
                                 _  => case (compare number 35.0) of {
                                         GT => <mkCN moderate_1_A inequality_N, but_1_Conj>;
                                         _  => case compare number 30.0 of {
                                                 GT => <mkCN moderate_1_A equality_1_N, and_Conj>;
                                                 _  => <mkCN high_1_A equality_1_N, and_Conj>
                                               }
                                       }
                               }
                       }
               };
        copula = case lang of {
                   "fre" => mkVP (mkAdv of_1_Prep income);
                   "rus" => mkVP amount_to_1_V2 income;
                   _     => mkVP income
                 } ;
        medIncome = mkS (mkCl (mkNP theSg_Det (mkCN median_3_A income_N)) copula) ;
        giniIndex = mkS (mkCl (mkNP theSg_Det (PossNP (mkCN distribution_1_N) (mkNP income_N))) (mkVP show_2_V2 (mkNP aSg_Det gini.p1))) 
    in [concat: 1 | mkPhrMark ( mkS gini.p2 medIncome giniIndex
                              | medIncome
                              | giniIndex
                              )];
           
    [concat: 1 | mkPhrMark (mkCl (mkNP theSg_Det (mkCN official_1_A currency_1_N)) (mkNP theSg_Det (expr e.P38.id)))];
    
    let number = QuantityNP (mkDecimal (round e.P1198.amount 2)) percent_MU;
        copula = case lang of {
                   "fre" => mkVP (mkAdv of_1_Prep number);
                   "rus" => mkVP amount_to_1_V2 number;
                   _     => mkVP number
                 }
    in [concat: 1 | mkPhrMark (mkCl (mkNP theSg_Det unemployment_N) copula)];
    
    let prep = case lang of {
                 "rus" => on_1_Prep;
                 _     => for_Prep
               };
        vats = [list: and_Conj |
                       mkNP' (QuantityNP (mkDecimal (round e.P2855.amount 2)) percent_MU) (mkAdv prep [list : and_Conj | mkNP (expr e.P2855.P518.id)])];
        copula = case lang of {
                   "fre" => mkVP (mkAdv of_1_Prep vats);
                   "rus" => mkVP amount_to_1_V2 vats;
                   _ => mkVP vats
                 }
    in [concat: 1 | mkPhrMark (mkCl (mkNP theSg_Det vat_1_N) copula)];

    let tax = [list : and_Conj | mkNP' (QuantityNP (mkDecimal (round e.P2834.amount 2)) percent_MU)
                                       (mkAdv above_Prep (QuantityNP (mkDecimal (round e.P2834.P2835.amount 2)) dollar_MU))];
        copula = case lang of {
                   "fre" => mkVP (mkAdv of_1_Prep tax);
                   "rus" => mkVP amount_to_1_V2 tax;
                   _ => mkVP tax
                 }
    in [concat: 1 | mkPhrMark (mkCl (mkNP theSg_Det income_tax_N) copula)];
    
    [concat |
       <h2 class="gp-page-title">climate_1_N</h2>
       let to_temp = \t -> case is_metric of {
                             True  => QuantityNP (mkDecimal (round t 2)) celsius_MU;
                             False => QuantityNP (mkDecimal (round (plusFloat (mulFloat t 1.8) 32.0) 2)) fahrenheit_MU
                           } ;
           maxNumber = to_temp e.P6591.amount;
           maxTemp = mkS TPastSimple
                         ( mkCl (mkNP (mkNP (mkDet the_Quant (mkOrd high_1_A)) (mkCN registered_2_A temperature_1_N)) (InLN (expr qid))) (mkVP reach_2_V2 maxNumber)
                         | mkCl (mkNP (mkDet the_Quant (mkOrd high_1_A)) (mkCN registered_2_A temperature_1_N)) (mkVP (mkVP reach_2_V2 maxNumber) (InLN (expr e.P6591.P276.id)))
                         );
           minNumber = to_temp e.P7422.amount;
           minVP = AdvVP (mkVP drop_4_V) (mkAdv to_2_Prep minNumber);
           minTemp = mkS TPastSimple
                         ( mkCl (mkNP (mkNP (mkDet the_Quant (mkOrd low_1_A)) (mkCN registered_2_A temperature_1_N))) (mkVP' (mkVP minVP (InLN (expr e.P7422.P276.id))) (time2adv e.P7422.P585.time))
                         | mkCl (mkNP (mkNP (mkDet the_Quant (mkOrd low_1_A)) (mkCN registered_2_A temperature_1_N)) (InLN (expr qid))) (mkVP' minVP (time2adv e.P7422.P585.time))
                         )
       in [concat' : 1 | mkPhrMark (mkS and_Conj minTemp maxTemp | minTemp | maxTemp)]
     ];

   </div>
