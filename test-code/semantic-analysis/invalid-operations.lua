-- Código de exemplo de erro do módulo typecheck.py

def main() {
    int integer;
    float floating_point;
    string str;

    -- Existem vários tipos de operações inválidas nas linhas abaixo.
    -- O compilador deve parar com uma mensagem de erro na primeira linha descomentada baixo

    str = str % floating_point;
    -- str = str / str
    -- floating_point = str * integer;
    -- str = str + floating_point;
    -- integer = floating_point % str;
}
