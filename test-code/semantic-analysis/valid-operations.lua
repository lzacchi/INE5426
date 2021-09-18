-- Code to test the correct function of
-- the typecheck modules

{
    int integer;
    float floating_point;
    string str;

    -- valid plus operations
    integer = integer + integer;
    floating_point = floating_point + floating_point;
    str = str + str;
    floating_point = integer + floating_point;
    floating_point = floating_point + integer;

    -- valid minus operations
    integer = integer - integer;
    floating_point = floating_point - floating_point;
    floating_point = integer - floating_point;
    floating_point = floating_point - integer;

    -- valid times operations
    integer = integer * integer;
    floating_point = floating_point * floating_point;
    floating_point = integer * floating_point;
    floating_point = floating_point * integer;

    -- valid division operations
    integer = integer / integer;
    floating_point = floating_point / floating_point;
    floating_point = integer / floating_point;
    floating_point = floating_point / integer;

    -- valid modulo operation
    integer = integer % integer;
}
