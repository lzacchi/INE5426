
int max_length;
max_length = 5;

string product_name;
product_name = new string[max_length];

string product_description;
product_description = new string[max_length];

float product_price;
product_price = new float[max_length];

def erase_index(int index){
    if (index >= max_length){
        if (index < 0){
            print("[ERROR] Invalid product index! Index should be between 0 and "+ string(max_length));
        } else {
            product_name[index] = "empty";
            product_description[index] = "empty";
            product_price[index] = -1.0;
            print("[LOG] Position "+index+" erased.");
        }
    } else {
        product_name[index] = "empty";
        product_description[index] = "empty";
        product_price[index] = -1.0;
        print("[LOG] Position "+index+" erased.");
    }

    return;
}

int j;
for (j = 0; j < max_length; j = j + 1){
    erase_index(j);
}

def product_info(int p_index){
    if (p_index >= 0){
        if (p_index < max_length){
            print("Product: "+ string(p_index));
            print("Name: " + product_name[p_index]);
            print("Description: " + product_description[p_index]);
            print("Price: $" + string(product_price[p_index]));
        } else {
            print("[ERROR] Invalid product index! Index should be between 0 and "+ string(max_length));
        }
    } else {
        print("[ERROR] Invalid product index! Index should be between 0 and "+ string(max_length));
    }

    return;
}

def add_product(string name, string description, float price){
    int i;
    int empty_slot;
    empty_slot = -1;

        for (i = 0; i < max_length; i = i + 1){
        if (product_name[i] == "empty"){
            print("Empty slot found");
            empty_slot = i;
        }
    }

    if (empty_slot <= -1){         print("[ERROR] There is not an empty slot to add a product!");
        return;

    } else {         print("[LOG] Adding product...");
        product_name[product_index] = name;
        product_description[product_index] = description;
        product_price[product_index] = price;
        print("[SUCCESS] Product Added!");
    }
}

def update_product(string name, string new_name, float new_price, string new_description){
        int i;
    int product_index;
    product_index = -1;

    print("[LOG] Searching for product which name is: '"+ name + "' ...");
    for (i = 0; i < max_length; i = i + 1){
        if (product_name[i] == name){
            print("Product:" + name + " found in position "+ i);
            product_index = i;
        }
    }

        if (product_index <= -1){
        print("[ERROR] Product not found. Are you sure that the product name is: "+ name);
    } else {
              print("[LOG] Updating...");
       product_name[product_index] = new_name;
       product_description[product_index] = new_description;
       product_price[product_index] = new_price;
       print("[SUCCESS] Update done!");
    }
    return;
}

def delete_product(string name){
        int i;
    int product_index;
    product_index = -1;

    print("[LOG] Searching for product which name is: '"+ name + "' ...");
    for (i = 0; i < max_length; i = i + 1){
        if (product_name[i] == name){
            print("Product:" + name + " found in position "+ i);
            product_index = i;
        }
    }

        if (product_index <= -1){
        print("[ERROR] Product not found. Are you sure that the product name is: "+ name);
    } else {
              print("[LOG] Deleting...");
       erase_index(product_index);
    }
    return;
}

add_product("programming in lua, book", "This book is a detailed and authoritative introduction to all aspects of Lua programming written by Lua's chief architect. ", 156.0);
add_product("laptop", "laptop lenovo ideapad s145", 2500.0);
add_product("echo dot third gen", "Amazon voice-controlled smart speaker that uses an artificially intelligent personal assistant", 250.0);
add_product("guitar", "giannini acoustic guitar 6 strings",1000.0);
add_product("moto g","Motorola Moto G with cracked screen", 800.0);

add_product("overflow", "Overflow test, this should not be added", 1.0);

delete_product("laptop");

update_product("guitar", "acoustic guitar", "giannini acoustic guitar 6 strings", 1200.0);

return;
}
