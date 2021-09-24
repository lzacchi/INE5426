--
-- smh.lua
--
-- Authors: Artur Barichello
--          Lucas Verdade
--          Lucas Zacchi

-- Código: smh.lua
-- SMH: Simple Math Helper
-- Algorithm: Math functions to help your code to be cleaner

def pow(float base, int exponent, float retval){
  int i;
  float mult;
  mult = retval;
  for (i = 0; i < exponent; i = i + 1){
    mult = mult * base;
  }
  print "Result:" ;
  print mult ;
}

def exp(int exponent, float retval){
  int euler_constant;
  euler_constant = 2.718;
  float mult;
  mult = retval;
  int i;
  for (i = 0; i < exponent; i = i + 1){
    mult = mult * euler_constant;
  }
  print "Result:" ;
  print mult ;
}

def abs(float number, float retval){
  float return_value;
  return_value = 1;
  return_value = number;
  if (number < 0){
    return_value = 1.0 * number;
  }
  print "Result:" ;
  print return_value ;
}

def floor(int number, float retval){
  float rest;
  rest = number % 1;
  float return_value;
  return_value = number - rest;
  print "Result:" ;
  print return_value ;
}

def ceil(int number, float retval){
  float rest;
  float return_value;
  rest = number % 1;
  return_value = number - rest;
  return_value = return_value + 1;
  print "Result:" ;
  print return_value ;
}

def round(int number, float retval){
  float rest;
  rest = number % 1;
  float return_value;
  if ( rest >= 0.5){
    return_value = number - rest;
    return_value = return_value + 1;
  } else {
    return_value = number - rest;
  }
  print "Result:" ;
  print return_value ;
}

def main(){
int euler_constant;
euler_constant = 2.718;
int tests;
tests = 1;
  int retval;
  retval = 1;
  int return_statement;
  if (tests == 1){
    print "Testing pow 3.0^2, expected value: 9.0" ;
    int arg1;
    int arg2;
    arg1 = 3.0;
    arg2 = 2.0;
    return_statement = pow(arg1, arg2, retval);

    print "Testing exp e^1, expected euler_constant which is: 2.718" ;
    arg1 = 1;
    return_statement = exp(arg1, retval);

    print "Testing abs(2.0), expected value: 2.0" ;
    arg1 = 2.0;
    return_statement = abs( arg1 , retval);

    print "Testing floor(3.9), expected value: 3.0" ;
    arg1 = 3.9;
    return_statement = floor( arg1, retval);

    print "Testing ceil(3.1), expected value: 4.0" ;
    arg1 = 3.1;
    return_statement = ceil( arg1, retval);

    print "Testing round(5.75), expected value: 6.0" ;
    arg1 = 5.75;
    return_statement = round( arg1, retval);
  }
}
