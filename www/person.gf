
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
	   "bul"|"spa" => presentTense;
       _           => [one: presentTense | (\_ -> pastTense) e.P570]
    } ;
    usePastTense = case lang of {
	   "bul" => presentTense;
       -- "spa" => TPastSimple;
       _     => pastTense
    } ;
    to_list_class = \l ->
      case compareInt l 5 of {
        LT => "gp-short-list" ;
        _  => case compareInt l 10 of {
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
     mkPhrMark (mkS (mkCl (expr qid) (mkVP (mkNP a_Quant [list: and_Conj | mkCN (gendered_expr e.P106.id e.P21.id)])))) 
     </p>

	 [concat | 
        <h2 class="gp-page-title">mkNP aPl_Det award_3_N</h2>
        let temp =
              case lang of {
                "fre" | "spa" => mkTemp useTense anteriorAnt ;
                _             => mkTemp usePastTense simultaneousAnt
              }
        in mkS temp positivePol (mkCl (mkNP pron) (mkVP receive_1_V2 (mkNP thePl_Det (mkCN following_2_A award_3_N)))) ;
        ":" ;
        <ul class=[len: to_list_class | e.P166]>[concat' | <li>(entity e.P166.id).label</li>]</ul>
        let prep = case lang of {
                     "spa" => to_1_Prep ;
                     _     => for_Prep
                   }
        in mkPhr (mkUtt (mkS useTense anteriorAnt (mkCl (mkNP pron) (mkVP (passiveVP (mkVPSlash nominate_1_V2)) (mkAdv prep (mkNP thePl_Det (mkCN following_2_A award_3_N))))))) ;
        ":" ;
        <ul class=[len: to_list_class | e.P1411]>[concat' | <li>(entity e.P1411.id).label</li>]</ul>
        ]
</div>


