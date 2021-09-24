--
-- smh.lua
--
-- Authors: Artur Barichello
--          Lucas Verdade
--          Lucas Zacchi

-- Código: smh.lua
-- SMH: Simple Math Helper
-- Algorithm: Math functions to help your code to be cleaner

-- global variables
int euler_constant = 2.718;

-- To run the main tests set the value to 1
-- To not run set to 0
int tests = 1;

-- Power Function
-- Calculate the base to the exponent power, as in base^exponent
def pow(float base, int exponent, float retval){
  retval = 1;
  for (i = 0 i < exponent; i++){
    retval = retval * base;
  }
  print("Result:");
  print(retval);
}

-- Calculate euler number exponential
--    euler_constant = 2.718;
-- Calculate euler_constant^exponent
def exp(int exponent, float retval){
  retval = 1;
  for (i = 0 i < exponent; i++){
    retval = retval * euler_constant;
  }
  print("Result:");
  print(retval);
}

-- Absolute value
-- Calculate the smallest integer greater than or equal to 'number'.
def abs(float number, float retval){
  retval = number;
  if (number < 0){
    retval = -1.0 * number;
  }
  print("Result:");
  print(retval);
}

-- Floor
-- Calculate the largest integer less than or equal to 'number'.
def floor(float number, float retval){
  float rest = number % 1;
  retval = number - rest;
  print("Result:");
  print(retval);
}

-- Ceil
-- rounds 'number' up to the next largest integer.
def ceil(float number, float retval){
  float rest = number % 1;
  retval = number - rest;
  retval = retval + 1;
  print("Result:");
  print(retval);
}

-- Round
-- Calculate the value of a number rounded to the nearest integer.
def round(float number, float retval){
  float rest = number % 1;
  if ( rest >= 0.5){
    retval = number - rest;
    retval = retval + 1;
  } else {
    retval = number - rest;
  }
  print("Result:");
  print(retval);
}

-- running tests
def main(){
  int retval;
  retval = 1;

  if (tests == 1){
    print("Testing pow 3.0^2, expected value: 9.0");
    pow(3.0, 2, retval);

    print("Testing exp e^1, expected euler_constant which is: 2.718");
    exp(1 , retval);

    print("Testing abs(-2.0), expected value: 2.0");
    abs( -2.0 , retval);

    print("Testing floor(3.9), expected value: 3.0");
    floor( 3.9, retval);

    print("Testing ceil(3.1), expected value: 4.0");
    ceil( 3.1, retval);

    print("Testing round(5.75), expected value: 6.0");
    round( 5.75, retval);
  }
}

main();
