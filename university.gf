let e = entity qid
in <div>
     <h1>expr qid</h1>

     <div class="infobox"><table border=1>
	    <tr><td><img src=(e.P18.s) width=250/></td></tr>
     </table></div>

	 <p>
     let cn        = mkCN' [list: and_Conj | mkCN (expr e.P31.id)] (mkAdv (expr e.P17.id)) ;
         inception = time2adv e.P571.time ;
         founder   = expr e.P112.id ;
         establish = [one | mkAP (mkVPSlash (mkVPSlash establish_4_V2) inception) founder
                          | mkAP (mkVPSlash (mkVPSlash establish_4_V2) inception)
                          | mkAP (mkVPSlash establish_4_V2) founder] ;
     in mkPhrMark (mkS (mkCl (mkNP (expr qid)) (mkVP (mkNP aSg_Det (mkCN establish cn)))));

     -- TODO: show the date
     [select: -1 | <mkPhrMark (mkS (mkCl (mkNP (mkDecimal <e.P2196.amount : Predef.Float>) studentMasc_1_N))),e.P2196.P585.time>] ;

     let office = entity e.P2388.id ;
         title  = [one | expr office.P279.id | presidentMasc_5_N] ;
         holder = [select: -1 | <expr {NP} office.P1308.id, office.P1308.P580.time>]
     in mkPhrMark (mkS (mkCl (mkNP theSg_Det (mkCN current_A title)) holder))
     </p>
   </div>