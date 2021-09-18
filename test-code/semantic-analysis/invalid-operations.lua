-- Code to test the correct function of
-- the typecheck modules.
--
-- The compiler should crash on the first invalid operations that is uncommented.

{
    int integer;
    float floating_point;
    string str;

    -- compiler stops on first error, uncomment only one line to test
    str = str % floating_point;
    -- str = str / str
    -- floating_point = str * integer;
    -- str = str + floating_point;
    -- integer = floating_point % str;
}