def small() {
    int small = 0;
    int smaller = 1;
    if (small < smaller) {
        int temp = smaller;
        smaller = small;
        int small = smaller;
        smaller = smaller + 1;
        small = small + 2;
    }
}
