



let e = entity qid;
    gender = case e.P21.id of {
	           "Q6581072" => she_Pron; 
               _ => he_Pron
    };
    pron = case lang of {
	   "spa" => ProDrop gender;
       _ => gender
    } ;
    useTense = case lang of {
	   "bul"|"spa" | "rus" => presentTense;
       _           => [one: presentTense | (\_ -> pastTense) e.P570]
    } ;
    usePastTense = case lang of {
	   "bul" => presentTense;
       -- "spa" => TPastSimple;
       _     => pastTense
    } ;
    to_list_class = \l ->
      case compare l 5 of {
        LT => "gp-short-list" ;
        _  => case compare l 10 of {
                LT => "gp-medium-list" ;
                _  => "gp-long-list"
              }
      }
in <div>
     <h1 class="gp-page-title"><expr qid : NP></h1>
     <div class="infobox">
     	<table border=1><tr><table>
        	<tr>[concat: 1 | <td><img src=(e.P18.s) width=250/></td>]</tr>
        	<tr>[concat: 1 | <td><img src=(e.P109.s) width=250/></td>]</tr>
    	</table></tr></table>
     </div>

     <p>
     -- add more descriptions
     let position   =
             [filter | <mkCN (gendered_expr e.P39.id e.P21.id), [one | [const: False | e.P39.P582.time] | True]>] ;
         occupation =
             [one | [list: and_Conj | mkCN (gendered_expr e.P106.id e.P21.id)]
                  | [const: (mkCN (gendered_expr "Q901" e.P21.id)) | e.P184.id]] ;
         occupation2 =
             [one | occupation
                  | case e.P21.id of {
                      "Q6581097" => mkCN man_1_N ;
                      "Q6581072" => mkCN woman_1_N
                    }
                  | mkCN human_N] ;

         dem      = [list: and_Conj | mkAP (demonym e.P27.id)] ;
         country  = [list: and_Conj | mkNP (expr e.P27.id)] ;

         intro : CN -> Phr = \desc ->
             mkPhrMark (mkS (mkCl (expr qid)
                                         (mkVP (mkNP (mkNP a_Quant
                              (mkCN (mkAP ( mkVPSlash (mkVPSlash (mkVPSlash bear_2_V2) (time2adv e.P569.time)) (InLN (expr e.P19.id))
                                          | mkVPSlash (mkVPSlash bear_2_V2) (time2adv e.P569.time)
                                          | mkVPSlash (mkVPSlash bear_2_V2) (mkAdv (expr e.P19.id))
                                          )) desc
                              | desc
                              ))))));

         extra_intro =
             mkPhrMark (mkS (mkCl (mkNP pron) (mkVP also_AdV (mkVP (mkNP aSg_Det (mkCN occupation)))))) ;

         p1 = <span>intro (mkCN dem position); extra_intro</span>
         p2 = <span>intro (mkCN position (mkAdv from_Prep (mkNP country))); extra_intro</span>
         p3 = <span>intro (mkCN position); extra_intro</span>
         p4 = <span>intro (mkCN position (mkAdv from_Prep (mkNP country)))</span>
         p5 = <span>intro (mkCN position)</span>
         p6 = <span>intro (mkCN dem occupation2)</span>
         p7 = <span>intro (mkCN occupation2 (mkAdv from_Prep (mkNP country)))</span>
         p8 = <span>intro (mkCN occupation2)</span>

     in [concat: 1 | p1 | p2 | p3 | p4 | p5 | p6 | p7 | p8] ;

     let advisors = [list: and_Conj | mkNP (expr e.P184.id)] ; 
         num = [len: (\l -> case compare l 1 of {
                              EQ => NumSg ;
                              _  => NumPl
                            }) | e.P184.id]
     in [concat : 1 |
            mkPhrMark (mkS useTense (mkCl (mkNP (DetQuant (PossPron gender) num) (mkCN doctoral_adviser_N)) advisors))];

     let teachers = [list: and_Conj | mkNP (expr e.P1066.id)]; 
         num = [len: (\l -> case compare l 1 of {
                              EQ => aSg_Det ;
                              _  => aPl_Det
                            }) | e.P1066.id]
     in [concat: 1 | mkPhrMark (mkS useTense (mkCl (mkNP pron) (mkNP aSg_Det (PossNP (mkCN (expr "Q48282")) teachers))))];
     
     let students = [list: and_Conj | mkNP (expr e.P802.id)] 
     in [concat: 1 | mkPhrMark (mkS useTense (mkCl (mkNP pron) (mkNP theSg_Det (PossNP (mkCN supervisorMasc_1_N) students))))];
     
     let native_langs = [list: and_Conj | mkNP (expr e.P103.id)];
         other_langs  = [list: and_Conj | mkNP (expr e.P1412.id)]; 
         num = [len: (\l -> case compare l 1 of {
                              EQ => NumSg ;
                              _  => NumPl
                            }) | e.P103.id];
         tense = case lang of {
                   "rus" => usePastTense; 
                   _     => useTense
                 };
         natLangPhr = mkS useTense (mkCl (mkNP (DetQuant (PossPron gender) num) (mkCN native_language_N)) native_langs) ;
      in [concat: 1 | mkPhrMark ( mkS but_1_Conj natLangPhr (mkS tense (mkCl (mkNP pron) (mkVP also_AdV (mkVP (SlashV2a speak_3_V2) other_langs))))
                                | natLangPhr
                                | mkS useTense (mkCl (mkNP pron) (mkVP (SlashV2a speak_3_V2) other_langs))
                                )] ;
     </p>
     
     -- add siblings
     
     [concat |
     	<h2 class="gp-page-title"> mkCN personal_1_A life_3_N </h2>
        let 
        aspect = case lang of {
            "fre" => AAnter;
            _ => ASimul};
        tense = case lang of {
            "fre" => useTense; 
            _ => usePastTense
            };
        prep = case lang of {
            "fre" => into_1_Prep;
            _ => in_1_Prep
        };
        parents = (ConjNP and_Conj (BaseNP (expr e.P25.id) (expr e.P22.id)));
        vp = case lang of {
            "fre" | "spa" | "rus" => mkCl (mkNP pron) (mkVP (mkVP be_born_V) (mkAdv prep (mkNP theSg_Det (PossNP (mkCN family_1_N) 
           parents))));
            _ => mkCl (mkNP pron) (mkVP (passiveVP bear_2_V2) (mkAdv in_1_Prep (mkNP theSg_Det 
            (PossNP (mkCN family_1_N) parents))))}
    
        in 
        [concat: 1 | mkPhrMark (variants {
        mkS useTense aspect vp;
        mkS useTense (mkCl (mkNP (DetQuant (PossPron gender) NumSg) (mkCN mother_1_N)) (mkNP (expr e.P25.id)));
        mkS useTense (mkCl (mkNP (DetQuant (PossPron gender) NumSg) (mkCN father_1_N)) (mkNP (expr e.P22.id)))
        })];
        
     
   	 -- spouse and children
     let 
     marryV2 = case lang of {
        "rus" => case e.P21.id of {
            "Q6581072" => marry_1b_V2; 
            _ => marry_1a_V2
        };
        _ => marry_1a_V2
      };
      marryIn = case lang of {
          "rus" => case e.P21.id of {
              "Q6581072" => marry_1b_V; 
              _ => marry_1a_V
          };
          _ => marry_in_V
      };
      marry = case lang of {
          "rus" => case e.P21.id of {
              "Q6581072" => marry_1b_V; 
              _ => marry_1a_V
          };
          _ => marry_1a_V};
          -- change to many
      spouse = [select: -1 | <entity e.P26.id, e.P26.P580.time>];
      name = [select: -1 | <expr e.P26.id, e.P26.P580.time>];
      -- occupation = [concat: 1 | expr spouse.P106.id];
      partners = entity e.P451.id;
      mPhr =  [list: and_Conj | 
      mkPhrMark (variants {mkS useTense (mkCl (mkNP pron) (mkVP (mkVP marryV2 (expr e.P26.id)) (InLN (expr e.P26.P2842.id))));
      mkS useTense (mkCl (mkNP pron) (mkVP marryV2 (expr e.P26.id)))})];
      marryVP = mkVP marryV2 
            (variants  {mkNP (mkCN (gendered_expr (entity e.P26.id).P106.id  (entity e.P26.id).P21.id) (expr e.P26.id));  mkNP (expr e.P26.id)})

      in
      [concat: 1 | variants { [concat | 
        variants {
        case e.P26.P1534.id of {
            "Q4" | "Q99521170" | "Q24037741" => [concat : 1 | mkPhrMark (variants {(mkS useTense (mkCl (mkNP pron) 
           (mkVP  marryVP (InLN (expr e.P26.P2842.id)))));
           (mkS useTense (mkCl (mkNP pron) marryVP))})];
              _ => [concat: 1 | mkPhrMark (variants {mkS useTense (mkCl (mkNP pron) (mkVP marryVP 
              (InLN (expr e.P26.P2842.id))));
              mkS useTense (mkCl (mkNP pron) (mkVP marryV2 (expr e.P26.id)))}); 
              mkPhrMark (mkS usePastTense (mkCl (mkNP they_Pron) (mkVP (mkVP divorce_2_V) (time2adv e.P26.P582.time))))]};
        [concat: 1 | mkPhrMark (variants {mkS useTense (mkCl (mkNP pron) (mkVP (mkVP marryV2 (expr e.P26.id)) (InLN (expr e.P26.P2842.id))));
        mkS useTense (mkCl (mkNP pron) (mkVP marryV2 (expr e.P26.id)))})]}]}] ;

      
     
     let 
     v = case e.P1196.id of {
          "Q149086" => passiveVP kill_1_V2;
          _ => mkVP die_1_V
          };
     v1 = variants {
          passiveVP kill_1_V2 (mkNP (expr e.P157.id)); 
          v;
          mkVP die_1_V
     } 
     in 
      [concat: 1 | mkPhrMark (mkS useTense (mkCl (mkNP pron)
      (mkVP (mkVP v1 (time2adv e.P570.time)) (mkAdv in_1_Prep (mkNP (expr e.P20.id))))))];

		];

     [concat |
     	<h2 class="gp-page-title"> education_2_N </h2>
        let universities = [list: and_Conj | mkNP (expr e.P69.id)] 
        in mkPhrMark (mkS usePastTense (mkCl (mkNP pron) (expr "P69" universities)))];
        
     
     [concat |
     	<h2 class="gp-page-title"> mkUtt (mkNP aPl_Det (mkCN notable_2_A work_2_N)) </h2>
        <ul class=[len: to_list_class | e.P800]> [concat' |<li>(entity e.P800.id).label</li>]</ul>];
     

	 [concat |
        <h2 class="gp-page-title">mkNP aPl_Det award_3_N</h2>
        let temp =
              case lang of {
                "fre" | "spa" => mkTemp useTense anteriorAnt ;
                _             => mkTemp usePastTense simultaneousAnt
              } ;
            prep = case lang of {
                     "spa" => to_1_Prep ;
                     _     => for_Prep
                   } ;
            awards =
              <ul class=[len: to_list_class | e.P166]>[concat' | <li>(entity e.P166.id).label</li>]</ul>
            nominations =
              <ul class=[len: to_list_class | e.P1411]>[concat' | <li>(entity e.P1411.id).label</li>]</ul> 
            p1 = <p>
                   mkS temp positivePol (mkCl (mkNP pron) (mkVP receive_1_V2 (mkNP thePl_Det (mkCN following_2_A award_3_N)))) ; ":" ;
                   awards ;
                   mkPhr (mkUtt (mkS useTense anteriorAnt (mkCl (mkNP pron) (mkVP (mkVP also_AdV (passiveVP (mkVPSlash nominate_1_V2))) (mkAdv prep (mkNP thePl_Det (mkCN following_2_A award_3_N))))))) ; ":" ;
                   nominations
                 </p>
            p2 = <p>
                   mkS temp positivePol (mkCl (mkNP pron) (mkVP receive_1_V2 (mkNP thePl_Det (mkCN following_2_A award_3_N)))) ; ":" ;
                   awards
                 </p>
            p3 = <p>
                   mkPhr (mkUtt (mkS useTense anteriorAnt (mkCl (mkNP pron) (mkVP (passiveVP (mkVPSlash nominate_1_V2)) (mkAdv prep (mkNP thePl_Det (mkCN following_2_A award_3_N))))))) ;
                   ":" ;
                   nominations
                 </p>
        in [one | p1 | p2 | p3]
     ]
</div>


