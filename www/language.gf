





let e   = entity qid ;
    cn0 = mkCN language_1_N ;
    cn1  = [one | ((case e.P279.id of {
                     --"Q1346342" => mkCN anglo_saxon_A cn0 ;
                     ("Q19814"| "Q1377152"|"Q3356483"|"Q147576") => mkCN romance_A cn0 ;
                     --"Q146665" => mkCN slavonic_1_A cn0 ;
                     ("Q26721"|"Q153050"|"Q1346342") => mkCN west_A (mkCN germanic_1_A cn0) ;
                     "Q146665" => mkCN south_A (mkCN slavonic_1_A cn0) ;
                     "Q145852" => mkCN west_A (mkCN slavonic_1_A cn0) ;
                     "Q149944" => mkCN east_A (mkCN baltic_1_A cn0) ;
                     "Q3090263" => mkCN north_A (mkCN germanic_1_A cn0) ;
                     "Q56356571" => mkCN western_1_A (mkCN iranian_A cn0) ;
                     "Q961559" => mkCN bantu_A cn0 ;
                     "Q34049" => mkCN semitic_1_A cn0 ;
                     "Q56433" => mkCN celtic_A cn0 ;
                     _ => variants {}
                   }) | cn0)] ;
    to_list_class = \l ->
      case compare l 5 of {
        LT => "gp-short-list" ;
        _  => case compare l 10 of {
                LT => "gp-medium-list" ;
                _  => "gp-long-list"
              }
      } ;
    cn2 = [one | (mkCN cn1 (mkRS(mkRCl (GenRP NumSg (UseN name_1_N)) (AdvVP (mkVP come_1_V) (mkAdv from_Prep (mkNP theSg_Det (mkCN (CompoundN country_1_N name_1_N) (mkNP (expr e.P138.id)))))))) | cn1)]

in <div>
   <h1 class="gp-page-title">expr qid</h1>
   <div class="infobox">
       <table border=1>
         <tr><td><table>
         <tr>
           <td>[concat: 1 | <img src=(e.P18.s) height=150/>]</td>
         </tr>
         <tr>
           <td>image_3_N</td>
         </tr>
         </table></td></tr> 
       </table>
     </div>
   <p> mkPhrMark (mkS (mkCl (mkNP (expr qid)) (mkNP aSg_Det cn2)))
   </p>

   <h2 class="gp-page-title">usage_1_N</h2>
   <div class="infobox">
       <table border=1>
         <tr><td><table>
         <tr>
           <td>[concat: 1 | <img src=(e.P1846.s) height=150/>]</td>
         </tr>
         <tr>
           <td>CompoundN distribution_1_N map_1_N</td>
         </tr>
         </table></td></tr> 
       </table>
     </div>
   let prep = case lang of {
                "fre" => into_1_Prep ;
                _     => in_1_Prep
              } ;
       num_people = [select: -1 | <mkDecimal e.P1098.amount, e.P1098.P585.time>] ;
       num_country = [len: (\l -> mkDecimal l) | e.P17.id]
       
       
   in [one | (mkCl (mkNP it_Pron) (mkVP (passiveVP speak_2_V2 (mkNP num_people people_1_N)) (mkAdv prep (mkNP num_country country_1_N))) | mkCl (mkNP it_Pron) (mkVP (passiveVP speak_2_V2 ) (mkAdv prep (mkNP num_country country_1_N))))] ;
      ":" ;
   <ul class=[len: to_list_class | e.P17]>[concat | <li>mkNP (expr e.P17.id)</li>]</ul>
   
  
   <h2 class="gp-page-title">grammar_N</h2>
   mkS (mkCl (mkNP (expr qid)) (mkVP have_2_V2 (mkNP aSg_Det (mkCN (mkCN (CompoundN sentence_1_N structure_2_N)) (mkAdv with_Prep (mkNP theSg_Det (mkCN following_2_A order_4_N)))))));
   ":";
   let svo = <span>subject_5_N ; "-" ; verb_1_N ; "-" ; object_3_N</span>
       sov = <span>subject_5_N ; "-" ; object_3_N ; "-" ; verb_1_N</span>
       ovs = <span>object_3_N ; "-" ; verb_1_N ; "-" ; subject_5_N</span>
       osv = <span>object_3_N ; "-" ; subject_5_N ; "-" ; verb_1_N</span>
       vso = <span>verb_1_N ; "-" ; subject_5_N ; "-" ; object_3_N</span>
       vos = <span>verb_1_N ; "-" ; object_3_N ; "-" ; subject_5_N</span>
       typ = case e.P4132.id of {
          "Q651641" => svo ;
          "Q539808" => sov ;
          "Q989463" => ovs ;
          "Q1417850" => osv ;
          "Q166097" => vso ;
          "Q568140" => vos ;
          _ => variants {}
       } 
       in typ ; "." ;
       
    <p>example_1_N ; ":" ;
       let source_lang = lang ;
           target_lang = case qid of {
             "Q1860" => "eng" ;
             "Q150" => "fre" ;
             "Q9027" => "swe" ;
             "Q7918" => "bul";
             "Q7411" => "dut" ;
             "Q1412" => "fin";
             "Q188" => "ger" ;
             "Q652" => "ita";
             "Q14196" => "afr";
             "Q7850" => "chi";
             "Q809" => "pol";
             "Q7913" => "ron";
             "Q7737" => "rus";
             "Q9176" => "kor";
             "Q10179" => "zul"
           } in
      <div>
       <table border=1>
         <tr>
           <td>source_lang</td>
           <td>linearize source_lang (mkCl (mkNP theSg_Det dog_1_N) (mkVP chase_1_V2 (mkNP theSg_Det cat_1_N)))</td>
         </tr>
         <tr>
           <td>target_lang</td>
           <td>linearize target_lang (mkCl (mkNP theSg_Det dog_1_N) (mkVP chase_1_V2 (mkNP theSg_Det cat_1_N)))</td>
         </tr>
       </table>
     </div>
    </p>   
    let num_mood = [len: (\l -> mkDecimal l) | e.P3161.id] ;
        num_tense = [len: (\l -> mkDecimal l) | e.P3103.id] ;
        mood = case e.P3161.id of {
		"Q682111" => mkCN indicative_A mood_3_N; -- need indicative_N in WordNet
        "Q473746" => UseN subjunctive_N ;
        "Q12021746" => UseN interrogative_2_N ;
        "Q22716" => UseN imperative_1_N ;
        "Q625581" => mkCN conditional_2_A mood_3_N; -- need conditional_N in WordNet
        "Q179230" => UseN infinitive_N ;
        "Q814722" => UseN participle_N ;
        _ => variants {}
        } ;
        list_mood = <span>"(" ; [list: and_Conj | mkNP mood] ; ")"</span>
    in
    <p> mkCl (mkNP (mkNP and_Conj (mkNP num_mood mood_3_N) (mkNP num_tense tense_N))(mkAdv in_1_Prep (mkNP (expr qid)))) ; ":" ;
    <ul> <li>mkNP aPl_Det mood_3_N ;
    <ul class=[len: to_list_class | e.P3161]>[concat | <li>mood</li>]</ul></li></ul>
    
    let prep = case lang of {
                "fre" => into_1_Prep ;
                _     => in_1_Prep
              } ;
    tense = case e.P3103.id of {
		"Q192613" => mkCN present_3_N ;
		"Q3910936" => mkCN simple_1_A present_3_N ;
    	"Q7240943" => mkCN (CompoundN present_3_N progressive_1_N) ;
    	"Q1240211" => mkCN (CompoundN present_3_N perfective_1_N) ;
    	"Q12738495" => mkCN (CompoundN (CompoundN present_3_N perfective_1_N) progressive_1_N) ;
        "Q11875867" => mkCN prophetic_A present_3_N ; -- liittopreesens in Finnish
        "Q1994301" => mkCN past_3_N ;
    	"Q1392475" => mkCN simple_1_A past_3_N ;
        "Q442485" => mkCN preterite_N ;
        "Q625420" => mkCN perfective_1_N ; -- would be great with perfect_N in the lexicon (imperfect_N already exists)
        "Q56650537" => mkCN (CompoundN past_3_N progressive_1_N) ;
    	"Q12547192" => mkCN (CompoundN past_3_N imperfect_N) ;
    	("Q13360204"|"Q22341188") => mkCN compound_1_A (CompoundN past_3_N perfective_1_N) ; -- passé composé
    	"Q56650537" => mkCN (CompoundN past_3_N progressive_1_N) ;
    	("Q23663136"|"Q623742") => mkCN (CompoundN past_3_N perfective_1_N) ; -- pluperfect
    	"Q1101896" => mkCN anterior_2_A past_3_N  ;
    	"Q12734727" => mkCN (CompoundN (CompoundN past_3_N perfective_1_N) progressive_1_N) ;
        "Q501405" => mkCN future_2_N ;
    	"Q1234617" => mkCN (CompoundN future_2_N perfective_1_N) ;
    	("Q1475560"|"Q20112616") => mkCN simple_1_A future_2_N ;
        "Q578167" => mkCN near_1_A future_2_N ;
    	"Q20472817" => mkCN (CompoundN (CompoundN future_2_N perfective_1_N) progressive_1_N) ;
    	"Q12743436" => mkCN (CompoundN future_2_N progressive_1_N) ;
        ("Q5492592"|"Q12274060") => mkCN future_2_N (mkAdv prep (mkNP theSg_Det (UseN past_3_N))) ; -- Q5492592 liittoimperfekti in Finnish
        "Q25619773" => mkCN conditional_1_A perfective_1_N ; -- would require the mood as conditional_N in the lexicon
        "Q3686414" => mkCN conditional_1_A present_3_N ; -- would require the mood as conditional_N in the lexicon
        "Q3502553" => mkCN subjunctive_A present_3_N ; -- would require the mood as subjunctive_N in the lexicon
        "Q3502544" => mkCN subjunctive_A past_3_N ; -- would require the mood as subjunctive_N in the lexicon
        "Q3502541" => mkCN subjunctive_A imperfect_N ; -- would require the mood as subjunctive_N in the lexicon
        "Q27955084" => mkCN subjunctive_A (CompoundN past_3_N perfective_1_N) ; -- would require the mood as subjunctive_N in the lexicon
        "Q52434162" => mkCN (CompoundN present_3_N imperative_1_N) ;
        "Q56319817" => mkCN (CompoundN past_3_N imperative_1_N) ;
        "Q52434245" => mkCN (CompoundN present_3_N infinitive_N) ;
        "Q52434302" => mkCN (CompoundN past_3_N infinitive_N) ;
        "Q10345583" => mkCN (CompoundN present_3_N participle_N) ;
        "Q12717679" => mkCN (CompoundN past_3_N participle_N) ;
        "Q52434511" => mkCN (CompoundN present_3_N gerund_N) ;
        "Q52434598" => mkCN (CompoundN past_3_N gerund_N) ;
        _ => variants {}
	}
	in
	<ul> <li>mkNP aPl_Det tense_N ;
	<ul class=[len: to_list_class | e.P3103]>[concat | <li>tense</li>]</ul></li></ul>
    </p>
   
   </div>
