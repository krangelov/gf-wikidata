
let e = entity qid;
in <div>
     <h1 class="gp-page-title">expr qid</h1>
     [concat: 1 |
        <div class="infobox"><table border=1>
	    <tr><td><img src=(e.P18.s) width=250/></td></tr>
	    </table></div>];
        
     <p>
     let np0 = [one | mkNP aSg_Det [list: and_Conj | mkCN (gendered_expr e.P279.id "Q6581097")]
                    | mkNP aSg_Det (mkCN kind_of_N2 (mkNP [list: and_Conj | mkCN (expr e.P31.id)]))] ;
         fields = mkNP aSg_Det [list: and_Conj | mkCN (expr e.P425.id)] ;
         np1 = mkNP' np0 (mkRS (mkRCl which_RP (mkVP (mkVP work_1_V) (mkAdv in_1_Prep (mkNP theSg_Det (mkCN (mkCN field_4_N) (mkAdv of_1_Prep (mkNP fields))))))))
     in mkPhrMark (mkS (mkCl (mkNP aSg_Det (expr qid)) np1))
     </p>
   </div>
