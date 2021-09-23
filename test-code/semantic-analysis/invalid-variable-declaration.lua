-- Código de demonstração da verificação de declarações de variáveis por escopo

{
    if (1 < 2) {
        print "OK - declaração de variavel dentro de escopo";
        int i;
        i = 3;
    }
    print "OK - declaração de variavel em escopo global";
    int i;
    print "ERRO - declaração de variável em mesmo escopo com mesmo nome";
    string i;
    i = "error!";
}
