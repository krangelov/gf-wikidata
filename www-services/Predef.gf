resource Predef = open Parse in {

param Bool = True | False ;

oper Int   : Type = variants {} ;          -- the type of integers
oper Float : Type = variants {} ;          -- the type of floats

oper entity : ({a} : Type) -> Str -> a = variants {} ;
oper int2digits  : Int -> Digits = variants {} ;
oper int2decimal : Int -> Decimal = variants {} ;
oper float2decimal : Float -> Decimal = variants {} ;
oper int2numeral : Int -> Numeral = variants {} ;
oper markup : ({a} : Type) -> a -> Str -> Str -> Str = variants {} ;
oper linearize : ({a} : Type) -> a -> Str = variants {} ;


oper lessInt : Int -> Int -> Bool = variants {} ;

}
