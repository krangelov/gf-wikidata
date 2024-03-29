resource Predef = open Parse in {

param Bool = True | False ;

oper Int   : Type = variants {} ;          -- the type of integers
oper Float : Type = variants {} ;          -- the type of floats

oper entity : ({a} : Type) -> Str -> a = variants {} ;
oper int2digits  : Int -> Digits = variants {} ;
oper int2decimal : Int -> Decimal = variants {} ;
oper float2decimal : Float -> Decimal = variants {} ;
oper int2numeral : Int -> Numeral = variants {} ;
oper markup : ({a} : Type) -> Str -> a -> Str -> Str = variants {} ;
oper linearize : ({a} : Type) -> a -> Str = variants {} ;
<<<<<<< Updated upstream
oper reset : ({a} : Type) -> a -> a = variants {} ;
oper first : ({a} : Type) -> a -> a = variants {} ;
=======
oper reset : Str -> Str = variants {} ;
>>>>>>> Stashed changes


oper lessInt : Int -> Int -> Bool = variants {} ;

}
