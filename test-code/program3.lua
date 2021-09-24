-- program3.lua
--
-- Authors: Artur Barichello
--          Lucas Verdade
--          Lucas Zacchi
-- Algorithm: Theater seats system

-- defining functions
def initialize_theater_system(int n_seats, string name){
    string theater_name;
    int max_seats;

    int free_seats_counter;
    int max_seats_counter;
    string reserved_seats;
    string suggestion_list;
    theater_name = name;
    max_seats = n_seats;
    reserved_seats = new string[max_seats][max_seats];
    max_seats_counter = max_seats * max_seats;
    free_seats_counter = max_seats * max_seats;
    suggestion_list = new string[4];
    int i;
    int j;
    for (i = 0; i<max_seats;i = i + 1){
        for (j = 0; j<max_seats;j = j + 1){
            reserved_seats[i][j] = "free";
        }
    }

    print "Welcome to " ;
    print theater_name ;
    print " seats system!" ;
    return;
}

def theater_status(){
    string theater_name;
    int max_seats;

    int free_seats_counter;
    int max_seats_counter;
    string reserved_seats;
    string suggestion_list;
    print "Total seats: " ;
    print theater_name ;
    print "Number of free seats: " ;
    print free_seats_counter ;
    print "Number of occupied seats: " ;
    print reserved_seats ;
    return;
}

def suggest_another_seat(int i, int j){
    string theater_name;
    int max_seats;

    int free_seats_counter;
    int max_seats_counter;
    string reserved_seats;
    string suggestion_list;

    int k;
    for (k=0; k < 4; k = k + 1){
        suggestion_list[k] = "";
    }

    if (i+1 < max_seats){
        if (reserved_seats[i+1][j] == "free"){
        suggestion_list[0] = i + j;
        }
    }
    if (j+1 < max_seats){
        if (reserved_seats[i][j+1] == "free"){
        suggestion_list[1] = i + j;
        }
    }
    if (i-1 >= 0){
        if (reserved_seats[i-1][j] == "free"){
        suggestion_list[2] = i + j;
        }
    }
    if (j-1 >= 0){
        if (reserved_seats[i][j-1] == "free"){
        suggestion_list[3] = i + j;
        }
    }

    print "Here are some free seats suggestions near from that one:" ;
    for (k = 0; k < 4; k = k + 1){
        print suggestion_list;
    }
    return;
}

def reserve_seat(int i, int j, string person_id){
    string theater_name;
    int max_seats;

    int free_seats_counter;
    int max_seats_counter;
    string reserved_seats;
    string suggestion_list;
    if (reserved_seats[i][j] == "free"){
        reserved_seats[i][j] = person_id;
        free_seats_counter = free_seats_counter -1;
    } else {
        print "Sorry! The seat in " ;
        print i ;
        print ", " ;
        print j ;
        print " is occupied." ;
    }
    return;
}

def free_seat(int i, int j){
    string theater_name;
    int max_seats;

    int free_seats_counter;
    int max_seats_counter;
    string reserved_seats;
    string suggestion_list;

    reserved_seats[i][j] = "free";
    free_seats_counter = free_seats_counter +1;
    print "Seat " ;
    print i ;
    print "," ;
    print j ;
    print " is free" ;
    return;
}
