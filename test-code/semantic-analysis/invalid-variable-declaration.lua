-- Código de demonstração da verificação de declarações de variáveis por escopo

def main() {
    if (1 < 2) {
        print "OK - declaração de variavel dentro de escopo";
        int i;
        i = 3;
    }
    print "OK - declaração de variavel em escopo global válida mesmo com ";
    print "nome utilizado anteriormente em outro escopo";
    int i;

    -- ///

    print "ERRO - declaração de variável em mesmo escopo com mesmo nome 'i'";
    string i;
    i = "error!";
}
