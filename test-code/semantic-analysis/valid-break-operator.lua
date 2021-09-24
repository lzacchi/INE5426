-- Código que demonstra o uso válido do operator 'break'

def main() {
    -- Uso válido dentro de um for
    int i;
    for (i = 0; i < 2; i = i + 1) {
        string str;
        str = "operator break válido!";
        break;
    }
}
