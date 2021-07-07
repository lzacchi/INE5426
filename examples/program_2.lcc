-- Exemplo 2
-- Algoritmo: 

int max_length;
max_length = 5;

string product_name;
product_name = new string[max_length];

string product_description;
product_description = new string[max_length];

float product_price;
product_price = new float[max_length];

-- TODO: initialize every product with empty or nil

def product_info(int p_index){
    if (p_index >= 0 && p_index < max_length){
        print("Product: "+ string(p_index));
        print("Name: " + product_name[p_index]);
        print("Description: " + product_description[p_index]);
        print("Price: $" + string(product_price[p_index]));
    } else {
        print("Invalid product index! Index should be between 0 and "+ string(max_length));
    }
}

def add_product(string name, string description, float price){
    -- checking slot
    int i;
    boolean available_slot = false;
    for (i = 0; i < max_length; i++){
        if (product_name[i] == "empty"){
            print("Empty slot found")
            available_slot = true;
        }
    }
    if (!available_slot){
        print("Error! There is not an empty slot to add a product!");
        return;
    }

     -- TODO: 
     -- push product handle
}

-- TODO: update function

-- TODO: delete function

