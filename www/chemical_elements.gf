let e = entity qid;

in <div>
     <h1 class="gp-page-title">expr qid</h1>
       <div class="infobox">
         <table border=1>
			<tr>
            	<td>[concat: 1 | <img src=(e.P18.s) width=100/>]</td>
            </tr>
            <tr> 
            	<td>mkCN chemical_1_A symbol_1_N</td>
            </tr>
         </table>
       </div>
       
       <p>        	
         	let el0 = [list: and_Conj | 
            	let el1 = case e.P31.id of {
                            "Q11344" => mkCN chemical_2_A (mkCN (expr e.P31.id));
                            _ => mkCN (mkCN (expr e.P31.id))
                        };	
            	in mkCN el1]
            in mkPhrMark (mkS (mkCl (mkNP (expr qid)) (mkNP aSg_Det el0)));
                  
            --use
            [concat: 1 | 
           	let use = (mkCN (expr e.P366.id))
               in mkPhrMark (mkS (mkCl (mkNP it_Pron) (mkVP (passiveVP use_1_V2) (mkAdv for_Prep (mkNP aPl_Det use)))))
               ];
               
            --discovered 
            [concat: 1 |
            	let disc = expr e.P61.id;
 	  				year = time2adv e.P61.P585.time
                in mkPhrMark (mkS (mkCl (mkNP (expr qid)) (mkVP (passiveVP discover_8_V2 disc) year)))];
            
            --named after
            [concat: 1 | 
                let orig = expr e.P138.id;
                    namer = expr e.P138.P3938.id;
                    year = time2adv e.P138.P580.time     

                    in mkPhrMark (mkS 
                    			and_Conj 
                                (mkS (mkCl (mkNP (mkDet it_Pron) name_1_N) (mkVP come_from_V2 (mkNP (mkCN orig)))))
                                (mkS (mkCl (mkNP it_Pron) (mkVP (passiveVP give_11_V2 namer) year))))
            ];
             
       </p>
  
</div>
     