-- Código de demonstração da verificação de tipos por escopo

{
    if (1 < 2) {
        print "declaração de variavel ok";
        int i;
        i = 3;
    }
    print "declaração de variavel ok";
    int i;
    print "erro de declaração de variável!";
    string i;
    i = "error!";
}
