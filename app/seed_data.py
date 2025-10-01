from models import Database

def seed_complete_database():
    """Seed database with all 20 countries and 5 dishes each"""
    db = Database()
    
    if db.dishes.count_documents({}) > 0:
        print("Database already contains dishes. Skipping seed.")
        return
    
    all_dishes = [
        # Italy (5 dishes)
        {"name": "Spaghetti Carbonara", "country": "Italy", "ingredients": ["spaghetti", "eggs", "bacon", "parmesan", "black pepper"], "instructions": "Cook pasta, mix with egg and cheese mixture, serve hot"},
        {"name": "Margherita Pizza", "country": "Italy", "ingredients": ["pizza dough", "tomato sauce", "mozzarella", "basil"], "instructions": "Top dough with sauce, cheese, and basil, then bake at high heat"},
        {"name": "Risotto Milanese", "country": "Italy", "ingredients": ["arborio rice", "saffron", "onion", "white wine", "parmesan"], "instructions": "Slowly cook rice with saffron-infused stock, stirring constantly"},
        {"name": "Tiramisu", "country": "Italy", "ingredients": ["ladyfingers", "coffee", "mascarpone", "cocoa powder"], "instructions": "Layer coffee-soaked cookies with mascarpone cream, chill overnight"},
        {"name": "Osso Buco", "country": "Italy", "ingredients": ["veal shanks", "tomatoes", "wine", "vegetables"], "instructions": "Braise veal shanks with vegetables and wine until tender"},

        # Japan (5 dishes)
        {"name": "Sushi Rolls", "country": "Japan", "ingredients": ["sushi rice", "nori", "fish", "wasabi", "soy sauce"], "instructions": "Form seasoned rice with fish and seaweed, serve with wasabi"},
        {"name": "Ramen Noodles", "country": "Japan", "ingredients": ["ramen noodles", "miso broth", "egg", "pork", "green onions"], "instructions": "Serve noodles in hot broth with toppings and soft-boiled egg"},
        {"name": "Tempura", "country": "Japan", "ingredients": ["shrimp", "vegetables", "tempura batter", "oil"], "instructions": "Deep fry lightly battered ingredients until golden and crispy"},
        {"name": "Yakitori", "country": "Japan", "ingredients": ["chicken", "tare sauce", "skewers"], "instructions": "Grill skewered chicken pieces with sweet soy-based glaze"},
        {"name": "Miso Soup", "country": "Japan", "ingredients": ["miso paste", "dashi", "tofu", "seaweed"], "instructions": "Dissolve miso in hot dashi broth, add tofu and wakame"},

        # India (5 dishes)
        {"name": "Butter Chicken", "country": "India", "ingredients": ["chicken", "tomato sauce", "cream", "garam masala"], "instructions": "Cook marinated chicken in rich, creamy tomato sauce"},
        {"name": "Biryani", "country": "India", "ingredients": ["basmati rice", "mutton", "saffron", "spices"], "instructions": "Layer fragrant spiced rice with meat, cook with saffron"},
        {"name": "Masala Dosa", "country": "India", "ingredients": ["rice batter", "potato filling", "coconut chutney"], "instructions": "Make thin crepe with fermented rice batter, fill with spiced potatoes"},
        {"name": "Tandoori Chicken", "country": "India", "ingredients": ["chicken", "yogurt", "tandoori spices"], "instructions": "Marinate chicken in spiced yogurt, cook in clay oven until charred"},
        {"name": "Dal Makhani", "country": "India", "ingredients": ["black lentils", "butter", "cream", "tomatoes"], "instructions": "Slow cook lentils with butter, cream and aromatic spices"},

        # Mexico (5 dishes)
        {"name": "Tacos al Pastor", "country": "Mexico", "ingredients": ["pork", "pineapple", "corn tortillas", "onion", "cilantro"], "instructions": "Serve marinated pork on small tortillas with fresh toppings"},
        {"name": "Guacamole", "country": "Mexico", "ingredients": ["avocados", "lime juice", "red onion", "cilantro", "jalapeño"], "instructions": "Mash ripe avocados with lime and seasonings until chunky"},
        {"name": "Chiles Rellenos", "country": "Mexico", "ingredients": ["poblano peppers", "cheese", "egg batter", "tomato sauce"], "instructions": "Stuff roasted peppers with cheese, coat in egg batter and fry"},
        {"name": "Mole Poblano", "country": "Mexico", "ingredients": ["dried chilies", "chocolate", "spices", "chicken"], "instructions": "Complex sauce with chocolate and chilies served over meat"},
        {"name": "Pozole Rojo", "country": "Mexico", "ingredients": ["hominy corn", "pork", "red chilies", "cabbage"], "instructions": "Traditional soup with hominy and meat, served with fresh garnishes"},

        # France (5 dishes)
        {"name": "Coq au Vin", "country": "France", "ingredients": ["chicken", "red wine", "mushrooms", "bacon"], "instructions": "Braise chicken in red wine with pearl onions and mushrooms"},
        {"name": "Ratatouille", "country": "France", "ingredients": ["eggplant", "zucchini", "tomatoes", "herbs de Provence"], "instructions": "Slow-cook Mediterranean vegetables with aromatic herbs"},
        {"name": "Croissant", "country": "France", "ingredients": ["puff pastry", "butter", "yeast"], "instructions": "Layer butter in yeasted dough, roll and shape, then bake until flaky"},
        {"name": "Bouillabaisse", "country": "France", "ingredients": ["mixed fish", "saffron", "fennel", "tomatoes"], "instructions": "Traditional Provençal fish stew with saffron and rouille sauce"},
        {"name": "Crème Brûlée", "country": "France", "ingredients": ["heavy cream", "egg yolks", "sugar", "vanilla"], "instructions": "Rich custard dessert with caramelized sugar crust on top"},

        # China (5 dishes)
        {"name": "Peking Duck", "country": "China", "ingredients": ["duck", "pancakes", "scallions", "hoisin sauce"], "instructions": "Roast duck with crispy skin, serve with thin pancakes and sauce"},
        {"name": "Kung Pao Chicken", "country": "China", "ingredients": ["chicken", "peanuts", "dried chilies", "soy sauce"], "instructions": "Stir-fry diced chicken with peanuts and spicy sauce"},
        {"name": "Mapo Tofu", "country": "China", "ingredients": ["silky tofu", "ground pork", "doubanjiang", "Sichuan peppercorns"], "instructions": "Braised tofu in spicy fermented bean sauce"},
        {"name": "Xiaolongbao", "country": "China", "ingredients": ["dumpling wrapper", "pork filling", "soup", "ginger"], "instructions": "Steamed soup dumplings filled with pork and hot broth"},
        {"name": "Sweet and Sour Pork", "country": "China", "ingredients": ["pork", "pineapple", "bell peppers", "sweet and sour sauce"], "instructions": "Battered pork with colorful vegetables in tangy sauce"},

        # Thailand (5 dishes)
        {"name": "Pad Thai", "country": "Thailand", "ingredients": ["rice noodles", "shrimp", "bean sprouts", "tamarind sauce"], "instructions": "Stir-fry noodles with protein and vegetables in sweet-tangy sauce"},
        {"name": "Tom Yum Goong", "country": "Thailand", "ingredients": ["shrimp", "lemongrass", "lime leaves", "chili"], "instructions": "Hot and sour soup with aromatic herbs and seafood"},
        {"name": "Green Curry", "country": "Thailand", "ingredients": ["green curry paste", "coconut milk", "chicken", "Thai basil"], "instructions": "Creamy curry with fresh herbs and coconut milk"},
        {"name": "Som Tam", "country": "Thailand", "ingredients": ["green papaya", "tomatoes", "lime", "fish sauce"], "instructions": "Refreshing salad of shredded papaya with spicy dressing"},
        {"name": "Mango Sticky Rice", "country": "Thailand", "ingredients": ["glutinous rice", "coconut milk", "ripe mango", "sugar"], "instructions": "Sweet coconut rice served with fresh mango slices"},

        # Greece (5 dishes)
        {"name": "Moussaka", "country": "Greece", "ingredients": ["eggplant", "ground lamb", "béchamel sauce", "tomatoes"], "instructions": "Layered casserole with eggplant, meat sauce and creamy topping"},
        {"name": "Greek Salad", "country": "Greece", "ingredients": ["tomatoes", "cucumbers", "feta cheese", "olives", "olive oil"], "instructions": "Fresh vegetables with feta and olives, dressed in olive oil"},
        {"name": "Souvlaki", "country": "Greece", "ingredients": ["pork", "lemon", "oregano", "pita bread"], "instructions": "Grilled meat skewers served with pita and tzatziki"},
        {"name": "Spanakopita", "country": "Greece", "ingredients": ["spinach", "feta cheese", "phyllo pastry", "herbs"], "instructions": "Flaky pastry filled with spinach and cheese mixture"},
        {"name": "Baklava", "country": "Greece", "ingredients": ["phyllo pastry", "nuts", "honey syrup", "cinnamon"], "instructions": "Sweet pastry layers with nuts and honey syrup"},

        # Spain (5 dishes)
        {"name": "Paella Valenciana", "country": "Spain", "ingredients": ["bomba rice", "chicken", "rabbit", "saffron", "vegetables"], "instructions": "Traditional rice dish cooked in wide, shallow pan"},
        {"name": "Gazpacho", "country": "Spain", "ingredients": ["tomatoes", "cucumbers", "peppers", "bread", "olive oil"], "instructions": "Cold soup made from fresh vegetables and bread"},
        {"name": "Jamón Ibérico", "country": "Spain", "ingredients": ["cured ham", "bread", "olive oil"], "instructions": "Thinly sliced cured ham served with bread and oil"},
        {"name": "Tortilla Española", "country": "Spain", "ingredients": ["potatoes", "eggs", "onions", "olive oil"], "instructions": "Thick potato omelet, a Spanish staple dish"},
        {"name": "Churros", "country": "Spain", "ingredients": ["flour", "water", "oil", "chocolate sauce"], "instructions": "Fried dough pastries served with thick chocolate for dipping"},

        # Brazil (5 dishes)
        {"name": "Feijoada", "country": "Brazil", "ingredients": ["black beans", "pork", "beef", "rice", "collard greens"], "instructions": "Traditional stew with beans and various meats"},
        {"name": "Açaí Bowl", "country": "Brazil", "ingredients": ["açaí berries", "banana", "granola", "honey"], "instructions": "Frozen açaí pulp topped with fruits and granola"},
        {"name": "Pão de Açúcar", "country": "Brazil", "ingredients": ["cassava flour", "cheese", "eggs", "milk"], "instructions": "Chewy cheese bread rolls, naturally gluten-free"},
        {"name": "Moqueca", "country": "Brazil", "ingredients": ["fish", "coconut milk", "dendê oil", "peppers"], "instructions": "Bahian fish stew with coconut milk and palm oil"},
        {"name": "Brigadeiro", "country": "Brazil", "ingredients": ["condensed milk", "cocoa powder", "butter", "chocolate sprinkles"], "instructions": "Sweet chocolate truffles rolled in sprinkles"},

        # Morocco (5 dishes)
        {"name": "Tagine", "country": "Morocco", "ingredients": ["lamb", "apricots", "almonds", "spices"], "instructions": "Slow-cooked stew in conical clay pot with dried fruits"},
        {"name": "Couscous", "country": "Morocco", "ingredients": ["couscous", "vegetables", "meat", "harissa"], "instructions": "Steamed semolina with vegetable and meat stew"},
        {"name": "Pastilla", "country": "Morocco", "ingredients": ["phyllo pastry", "pigeon", "almonds", "cinnamon"], "instructions": "Sweet and savory pie with meat filling and nuts"},
        {"name": "Harira", "country": "Morocco", "ingredients": ["lentils", "tomatoes", "cilantro", "lamb"], "instructions": "Traditional soup often eaten during Ramadan"},
        {"name": "Mint Tea", "country": "Morocco", "ingredients": ["green tea", "fresh mint", "sugar"], "instructions": "Sweet tea ceremony drink poured from height"},

        # Lebanon (5 dishes)
        {"name": "Hummus", "country": "Lebanon", "ingredients": ["chickpeas", "tahini", "lemon", "garlic"], "instructions": "Creamy dip made from blended chickpeas and sesame paste"},
        {"name": "Tabbouleh", "country": "Lebanon", "ingredients": ["parsley", "tomatoes", "bulgur", "lemon", "mint"], "instructions": "Fresh herb salad with bulgur and lemon dressing"},
        {"name": "Manakish", "country": "Lebanon", "ingredients": ["flatbread", "za'atar", "olive oil", "cheese"], "instructions": "Breakfast flatbread topped with herb blend and oil"},
        {"name": "Kibbeh", "country": "Lebanon", "ingredients": ["bulgur", "meat", "onions", "pine nuts"], "instructions": "Fried croquettes of bulgur wheat and seasoned meat"},
        {"name": "Fattoush", "country": "Lebanon", "ingredients": ["mixed greens", "pita bread", "sumac", "vegetables"], "instructions": "Salad with crispy pita chips and tangy sumac dressing"},

        # Peru (5 dishes)
        {"name": "Ceviche", "country": "Peru", "ingredients": ["raw fish", "lime juice", "red onions", "cilantro"], "instructions": "Fresh fish 'cooked' in citric acid with herbs"},
        {"name": "Lomo Saltado", "country": "Peru", "ingredients": ["beef strips", "french fries", "tomatoes", "soy sauce"], "instructions": "Stir-fried beef with vegetables and crispy potatoes"},
        {"name": "Ají de Gallina", "country": "Peru", "ingredients": ["chicken", "yellow peppers", "bread", "nuts"], "instructions": "Creamy chicken stew with spicy yellow pepper sauce"},
        {"name": "Anticuchos", "country": "Peru", "ingredients": ["beef heart", "ají panca", "cumin", "skewers"], "instructions": "Grilled beef heart skewers with spicy marinade"},
        {"name": "Suspiro Limeño", "country": "Peru", "ingredients": ["condensed milk", "egg yolks", "port wine", "meringue"], "instructions": "Sweet dessert with caramel base and light meringue top"},

        # Argentina (5 dishes)
        {"name": "Asado", "country": "Argentina", "ingredients": ["beef ribs", "chorizo", "chimichurri", "salt"], "instructions": "Traditional barbecue with various cuts of meat"},
        {"name": "Empanadas", "country": "Argentina", "ingredients": ["pastry dough", "beef filling", "onions", "spices"], "instructions": "Baked pastries filled with seasoned meat and vegetables"},
        {"name": "Milanesa", "country": "Argentina", "ingredients": ["beef cutlet", "breadcrumbs", "eggs", "herbs"], "instructions": "Breaded and fried beef cutlet, served with lemon"},
        {"name": "Dulce de Leche", "country": "Argentina", "ingredients": ["milk", "sugar", "vanilla"], "instructions": "Sweet caramel spread made from slowly cooked milk"},
        {"name": "Provoleta", "country": "Argentina", "ingredients": ["provolone cheese", "oregano", "red pepper flakes"], "instructions": "Grilled provolone cheese with herbs and spices"},

        # Russia (5 dishes)
        {"name": "Borscht", "country": "Russia", "ingredients": ["beetroot", "cabbage", "beef", "sour cream"], "instructions": "Hearty soup with beets, served hot with sour cream"},
        {"name": "Beef Stroganoff", "country": "Russia", "ingredients": ["beef strips", "mushrooms", "sour cream", "onions"], "instructions": "Tender beef in creamy mushroom sauce"},
        {"name": "Pelmeni", "country": "Russia", "ingredients": ["dumpling dough", "meat filling", "butter", "dill"], "instructions": "Small dumplings filled with meat, served with butter"},
        {"name": "Blini", "country": "Russia", "ingredients": ["flour", "eggs", "milk", "caviar"], "instructions": "Thin pancakes traditionally served with caviar or jam"},
        {"name": "Olivier Salad", "country": "Russia", "ingredients": ["potatoes", "carrots", "eggs", "mayonnaise", "pickles"], "instructions": "Traditional potato salad with vegetables and mayonnaise"},

        # Turkey (5 dishes)
        {"name": "Kebab", "country": "Turkey", "ingredients": ["lamb", "yogurt", "pita bread", "vegetables"], "instructions": "Grilled meat served with yogurt sauce and vegetables"},
        {"name": "Baklava", "country": "Turkey", "ingredients": ["phyllo pastry", "pistachios", "honey", "butter"], "instructions": "Sweet pastry with nuts and honey syrup"},
        {"name": "Meze Platter", "country": "Turkey", "ingredients": ["hummus", "dolma", "olives", "cheese"], "instructions": "Selection of small dishes served as appetizers"},
        {"name": "Turkish Delight", "country": "Turkey", "ingredients": ["starch", "sugar", "rosewater", "pistachios"], "instructions": "Sweet confection flavored with rosewater and nuts"},
        {"name": "Lahmacun", "country": "Turkey", "ingredients": ["thin dough", "minced meat", "vegetables", "herbs"], "instructions": "Thin pizza-like flatbread topped with meat and herbs"},

        # Ethiopia (5 dishes)
        {"name": "Injera", "country": "Ethiopia", "ingredients": ["teff flour", "water", "starter culture"], "instructions": "Spongy sourdough flatbread, the base of Ethiopian meals"},
        {"name": "Doro Wat", "country": "Ethiopia", "ingredients": ["chicken", "berbere spice", "onions", "eggs"], "instructions": "Spicy chicken stew with hard-boiled eggs"},
        {"name": "Kitfo", "country": "Ethiopia", "ingredients": ["raw beef", "mitmita spice", "butter", "cheese"], "instructions": "Ethiopian steak tartare with spiced butter"},
        {"name": "Vegetarian Combo", "country": "Ethiopia", "ingredients": ["lentils", "cabbage", "collard greens", "berbere"], "instructions": "Mixed vegetarian dishes served on injera bread"},
        {"name": "Ethiopian Coffee", "country": "Ethiopia", "ingredients": ["green coffee beans", "incense", "sugar"], "instructions": "Traditional coffee ceremony with roasted beans"},

        # South Korea (5 dishes)
        {"name": "Kimchi", "country": "South Korea", "ingredients": ["napa cabbage", "gochugaru", "garlic", "ginger"], "instructions": "Fermented spicy cabbage, Korea's national dish"},
        {"name": "Bibimbap", "country": "South Korea", "ingredients": ["rice", "vegetables", "beef", "gochujang", "egg"], "instructions": "Mixed rice bowl with vegetables, meat and spicy sauce"},
        {"name": "Korean BBQ", "country": "South Korea", "ingredients": ["bulgogi beef", "lettuce", "ssamjang", "garlic"], "instructions": "Grilled marinated beef wrapped in lettuce leaves"},
        {"name": "Japchae", "country": "South Korea", "ingredients": ["sweet potato noodles", "vegetables", "soy sauce", "sesame oil"], "instructions": "Stir-fried glass noodles with colorful vegetables"},
        {"name": "Hotteok", "country": "South Korea", "ingredients": ["flour dough", "brown sugar", "cinnamon", "nuts"], "instructions": "Sweet pancakes filled with sugar and nuts, popular street food"}
    ]
    
    result = db.dishes.insert_many(all_dishes)
    print(f"Successfully seeded {len(result.inserted_ids)} dishes from 20 countries")
    return len(result.inserted_ids)

if __name__ == "__main__":
    seed_complete_database()
