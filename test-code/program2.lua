def initializing_globals(){
    int max_length;
    max_length = 5;

    string product_name;
    product_name = new string[max_length];

    string product_description;
    product_description = new string[max_length];

    float product_price;
    product_price = new float[max_length];

    int j;
    for (j = 0; j < max_length; j = j + 1){
        if (j >= max_length){
            if (j < 0){
                print "[ERROR] Invalid product index! Index should be between 0 and " ;
                print  max_length ;
            } else {
                product_name[j] = "empty";
                product_description[j] = "empty";
                product_price[j] = 1.0;
                print "[LOG] Position " ;
                print j ;
                print " erased." ;
            }
        } else {
            product_name[j] = "empty";
            product_description[j] = "empty";
            product_price[j] = 1.0;
            print "[LOG] Position " ;
            print j ;
            print " erased." ;
        }
    }
}

def product_info(int p_index){
    int max_length;
    max_length = 5;

    string product_name;
    product_name = new string[max_length];

    string product_description;
    product_description = new string[max_length];

    float product_price;
    product_price = new float[max_length];
    if (p_index >= 0){
        if (p_index < max_length){
            print "Product: " ;
            print  p_index ;
            print "Name: "  ;
            print  product_name[p_index] ;
            print "Description: "  ;
            print  product_description[p_index] ;
            print "Price: $"  ;
            print  product_price[p_index] ;
        } else {
            print "[ERROR] Invalid product index! Index should be between 0 and " ;
            print  max_length ;
        }
    } else {
        print "[ERROR] Invalid product index! Index should be between 0 and " ;
        print  max_length ;
    }

    return;
}

def add_product(string name, string description, float price){
    int max_length;
    max_length = 5;

    string product_name;
    product_name = new string[max_length];

    string product_description;
    product_description = new string[max_length];

    float product_price;
    product_price = new float[max_length];
    int i;
    int empty_slot;
    empty_slot = 1;

    for (i = 0; i < max_length; i = i + 1){
        if (product_name[i] == "empty"){
            print "Empty slot found" ;
            empty_slot = i;
        }
    }

    if (empty_slot == 1){
        print "[ERROR] There is not an empty slot to add a product!" ;
        return;

    } else {
        print "[LOG] Adding product..." ;
        product_name[empty_slot] = name;
        product_description[empty_slot] = description;
        product_price[empty_slot] = price;
        print "[SUCCESS] Product Added!" ;
    }
}

def update_product(string name, string new_name, float new_price, string new_description){
    int max_length;
    max_length = 5;

    string product_name;
    product_name = new string[max_length];

    string product_description;
    product_description = new string[max_length];

    float product_price;
    product_price = new float[max_length];
    int i;
    int product_index;
    product_index = 1;

    print "[LOG] Searching for product which name is: '" ;
    print  name  ;
    print  "' ..." ;
    for (i = 0; i < max_length; i = i + 1){
        if (product_name[i] == name){
            print "Product:"  ;
            print  name  ;
            print  " found in position " ;
            print  i ;
            product_index = i;
        }
    }

    if (product_index <= 1){
        print "[ERROR] Product not found. Are you sure that the product name is: " ;
        print  name ;
    } else {
       print "[LOG] Updating..." ;
       product_name[product_index] = new_name;
       product_description[product_index] = new_description;
       product_price[product_index] = new_price;
       print "[SUCCESS] Update done!" ;
    }
    return;
}

def delete_product(string name){
    int max_length;
    max_length = 5;

    string product_name;
    product_name = new string[max_length];

    string product_description;
    product_description = new string[max_length];

    float product_price;
    product_price = new float[max_length];
    int i;
    int product_index;
    product_index = 1;

    print "[LOG] Searching for product which name is: '" ;
    print  name  ;
    print  "' ..." ;
    for (i = 0; i < max_length; i = i + 1){
        if (product_name[i] == name){
            print "Product:"  ;
            print  name  ;
            print  " found in position " ;
            print  i ;
            product_index = i;
        }
    }

    if (product_index <= 1){
        print "[ERROR] Product not found. Are you sure that the product name is: " ;
        print  name ;
    } else {
        print "[LOG] Deleting..." ;
       if (product_index >= max_length){
            if (product_index < 0){
                print "[ERROR] Invalid product index! Index should be between 0 and " ;
                print  max_length ;
            } else {
                product_name[product_index] = "empty";
                product_description[product_index] = "empty";
                product_price[product_index] = 1.0;
                print "[LOG] Position " ;
                print product_index ;
                print " erased." ;
            }
        } else {
            product_name[product_index] = "empty";
            product_description[product_index] = "empty";
            product_price[product_index] = 1.0;
            print "[LOG] Position " ;
            print product_index ;
            print " erased." ;
        }
    }
    return;
}
