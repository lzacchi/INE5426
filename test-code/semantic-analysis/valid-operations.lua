-- Código de exemplo para demonstrar o funcionamento
-- do módulo typecheck.py

def main() {
    int integer;
    float floating_point;
    string str;

    integer = 10;
    floating_point = 5.0;
    str = "Dez";

    -- Operações válidas de soma
    integer = integer + integer;
    floating_point = floating_point + floating_point;
    str = str + str;
    floating_point = integer + floating_point;
    floating_point = floating_point + integer;

    -- Operações válidas de subtração
    integer = integer - integer;
    floating_point = floating_point - floating_point;
    floating_point = integer - floating_point;
    floating_point = floating_point - integer;

    -- Operações válidas de multiplicação
    integer = integer * integer;
    floating_point = floating_point * floating_point;
    floating_point = integer * floating_point;
    floating_point = floating_point * integer;

    -- Operações válidas de divisão
    integer = integer / integer;
    floating_point = floating_point / floating_point;
    floating_point = integer / floating_point;
    floating_point = floating_point / integer;

    -- Operações válidas de módulo
    integer = integer % integer;
}
