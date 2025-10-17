let e = entity qid;
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
         [concat: 1 | <tr><td><img src=(e.P18.s) width=250/></td></tr>] ;
         [concat: 1 | <tr><td><img src=(e.P242.s) width=250/></td></tr>]
       </table>
     </div>

     <p>
     -- country and population
     let
        descr =
          [one | case <e.P31.id, compare e.P1376.id e.P17.id> of {
                   <"Q51929311",EQ> => mkNP (mkNP and_Conj (mkNP (mkDet the_Quant (mkOrd large_1_A)) city_1_N)
                                                           (mkNP theSg_Det capital_3_N))
                                            (mkAdv of_1_Prep (mkNP (expr e.P17.id))) ;
                   _ => variants {}
                 }
               | case compare e.P1376.id e.P17.id of {
                   EQ => mkNP (mkNP theSg_Det capital_3_N)
                              (mkAdv of_1_Prep (mkNP (expr e.P17.id))) ;
                   _  => variants {}
                 }
               | case <e.P31.id, compare e.P1376.id e.P17.id> of {
                   <"Q51929311",EQ> => mkNP (mkNP (mkDet the_Quant (mkOrd large_1_A)) city_1_N)
                                            (mkAdv (expr e.P17.id)) ;
                   _ => variants {}
                 }
               | let cn0 = [one | [list: and_Conj | mkCN (expr e.P31.id)] | mkCN city_1_N] ;
                     cn1 = mkCN' cn0 [one | [select: -1 | <mkAdv (expr e.P17.id),e.P17.P580.time>]
                                          | mkAdv (expr e.P17.id)];
                 in mkNP aSg_Det cn1
               ] ;

        population = [select: -1 | <mkNP (mkDet (mkDecimal <e.P1082.amount : Predef.Int>)) (mkCN inhabitantMasc_1_N),e.P1082.P585.time>]
     in case lang of {
         "fin" => [concat: 1 | mkPhrMark (mkS (mkCl (mkNP (expr qid)) descr)) ;
                               mkPhrMark (mkS (ExistNPAdv population there_1_Adv))] ;
         _     => [concat: 1 | mkPhrMark (mkS (mkCl (mkNP (expr qid)) (mkVP (mkNP' descr (mkAdv with_Prep population)))))]
       };

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

    -- TODO: family relation?
    let officeGov = entity e.P1313.id ;
        name      = [select: -1 | <expr e.P6.id, e.P6.P580.time>];
        prev_name = [select: -2 | <expr e.P6.id, e.P6.P580.time>]
    in [concat: 1 | mkPhrMark (mkCl (mkNP the_Det (mkCN current_A mayor_N))
                                    ( ExtRelNP (mkNP (mkCN (expr officeGov.P279.id) name))
                                               (mkRS TPastSimple (mkRCl which_RP (mkVP (mkVP take_office_V)
                                                                                       (mkAdv after_Prep prev_name))))
                                    | mkNP (mkCN (expr officeGov.P279.id) name)
                                    | name
                                    ))] ;
    </p>

    [concat: 1 |
       <h2 class="gp-page-title">mkNP aPl_Det (mkCN administrative_A unit_3_N)</h2>
       
       mkPhr (mkCl (mkNP theSg_Det city_1_N)
                   (mkVP have_1_V2 (mkNP thePl_Det 
                                         (mkCN following_2_A (mkCN administrative_A unit_3_N))))); ":" ;

       <ul class=[len: to_list_class | e.P150]>[concat' | <li>(entity e.P150.id).label</li>]</ul>];

    <h2 class="gp-page-title">economy_1_N</h2>
    -- fix growth
    
    let gdp0 = QuantityNP (mkDecimal (round e.P2131.amount 2)) dollar_MU ;
        gdp  = [default: gdp0 | mkNP and_Conj gdp0
		                             (mkNP (QuantityNP (mkDecimal (round e.P2132.amount 2)) dollar_MU) per_capita_Adv)];
        growth = case compare e.P2219.amount 0.0 of {
    	           GT => growth_3_N;
                   _  => decline_1_N
                 };
	    number = mkNP' (mkNP gdp) (mkAdv with_Prep 
                                         (mkNP (mkNP aSg_Det growth)
                                               (mkAdv of_1_Prep (QuantityNP (mkDecimal (round e.P2219.amount 2)) percent_MU))));
	    copula = case lang of {
                   "fre" => mkVP (mkAdv of_1_Prep number);
                   "rus" => mkVP amount_to_1_V2 number;
                   _     => mkVP number
                 }
    in [concat : 1 | mkPhrMark (mkCl (mkNP theSg_Det gross_domestic_product_N) copula)];

    -- gdp 
    let number = (QuantityNP (mkDecimal (round e.P1279.amount 2)) percent_MU);
        copula = case lang of {
                   "fre" => mkVP (mkAdv of_1_Prep number);
                   "rus" => (mkVP amount_to_1_V2 number);
                   _ => mkVP number
                 }
    in [concat: 1 | mkPhrMark (mkCl (mkNP theSg_Det (CompoundN inflation_1_N rate_4_N)) copula)];
   </div>
