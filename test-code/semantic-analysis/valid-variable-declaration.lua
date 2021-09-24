-- Código de demonstração da verificação de declarações de variáveis por escopo

def main() {
    print "OK - declaração de variavel em escopo da função 'main'";
    int a;
    a = 2;
}

def util() {
    int i;
    for (i = 0; i < 2; i = i + 1) {
        print "OK - declaração de variavel com nome igual porém utilizado anteriormente em outro escopo";
        int a;
        print "loop!";
    }

    print "OK - declaração de variavel com nome igual porém utilizado em outro escopo anteriormente";
    int a;
    a = 5;
}
