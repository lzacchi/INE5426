--
-- program3.lua
--
-- Authors: Artur Barichello
--          Lucas Verdade
--          Lucas Zacchi
-- Algorithm: Theater seats system

-- declaring global variables
string theater_name;
int max_seats;

int free_seats_counter; 
int max_seats_counter; -- max seats in theater
string reserved_seats; -- matrix of seats that are 'free' or has person id that reserved it
string suggestion_list;

-- defining functions
def initialize_theater_system(int n_seats, string name){
    -- initialazing global variables
    theater_name = name;
    max_seats = n_seats;
    reserved_seats = new string[max_seats][max_seats];
    max_seats_counter = max_seats * max_seats;
    free_seats_counter = max_seats * max_seats;
    suggestion_list = new string[4];
    -- initalize seats
    int i;
    int j;
    for (i=0; i<max_seats;i++){
        for (j=0; j<max_seats;j++){
            reserved_seats[i][j] = "free";
        }
    }

    print("Welcome to "+theater_name+" seats system!");
    return;
}

def theater_status(){
    print("Total seats: "+theater_name);
    print("Number of free seats: "+free_seats_counter);
    print("Number of occupied seats: "+reserved_seats);
    return; 
}

def suggest_another_seat(int i, int j){
    -- clear suggestion list
    for (k=0; k < 4; k++){
        suggestion_list[k] = "";
    }

    -- searching for nearby free seats
    if (i+1 < max_seats && reserved_seats[i+1][j] == "free"){
        suggestion_list[0] = i +","+j;
    }
    if (j+1 < max_seats && reserved_seats[i][j+1] == "free"){
        suggestion_list[1] = i +","+j;
    }
    if (i-1 >= 0 && reserved_seats[i-1][j] == "free"){
        suggestion_list[2] = i +","+j;
    }
    if (j-1 >= 0 && reserved_seats[i][j-1] == "free"){
        suggestion_list[3] = i +","+j;
    }
    
    int k;
    print("Here are some free seats suggestions near from that one:")
    for (k=0; k < 4; k++){
        print(suggestion_list[k]);
    }
    return;
}

-- Reserve function that suggest another seats if that one is occupied.
def reserve_seat(int i, int j, string person_id){
    if (reserved_seats[i][j] == "free"){
        reserved_seats[i][j] = person_id;
        free_seats_counter = free_seats_counter -1;
    } else {
        print("Sorry! The seat in "+i+", "+j+" is occupied.");
        suggest_another_seat(i, j);
    }
    return;
}

def free_seat(int i, int j){
    reserved_seats[i][j] = "free";
    free_seats_counter = free_seats_counter +1;
    print("Seat "+i+","+j+" is free");
    return;
}

def main(){
    initialize_theater_system(5, "Praia de Belas Cinema");
    theater_status();

    -- simulating a client reserving the seat in 1,1
    reserve_seat(1,1,"LucasV");

    -- simulating a client trying to reserve and occupied seat (1,1)
    reserve_seat(1,1,"ArturB");
    return;
}

-- run:
main();
