"""
GeoDish Seed Data - Single Source of Truth
All countries and dishes defined here
"""

# Complete seed data for all 25 countries
GEODISH_SEED_DATA = [
    # Italy (5 dishes)
    {"name": "Spaghetti Carbonara", "country": "Italy", "ingredients": ["spaghetti", "eggs", "bacon", "parmesan", "black pepper"], "instructions": "Cook pasta, mix with egg and cheese mixture"},
    {"name": "Margherita Pizza", "country": "Italy", "ingredients": ["pizza dough", "tomato sauce", "mozzarella", "basil"], "instructions": "Top dough with sauce, cheese, and basil, then bake"},
    {"name": "Risotto Milanese", "country": "Italy", "ingredients": ["arborio rice", "saffron", "onion", "white wine", "parmesan"], "instructions": "Slowly cook rice with saffron and stock"},
    {"name": "Tiramisu", "country": "Italy", "ingredients": ["ladyfingers", "coffee", "mascarpone", "cocoa powder"], "instructions": "Layer coffee-soaked cookies with mascarpone cream"},
    {"name": "Osso Buco", "country": "Italy", "ingredients": ["veal shanks", "tomatoes", "wine", "vegetables"], "instructions": "Braise veal shanks with vegetables and wine"},
    
    # France (5 dishes)
    {"name": "Coq au Vin", "country": "France", "ingredients": ["chicken", "red wine", "mushrooms", "bacon"], "instructions": "Braise chicken in red wine with vegetables"},
    {"name": "Ratatouille", "country": "France", "ingredients": ["eggplant", "zucchini", "tomatoes", "herbs"], "instructions": "Stew Mediterranean vegetables together"},
    {"name": "Croissant", "country": "France", "ingredients": ["puff pastry", "butter"], "instructions": "Layer butter in dough, roll and bake"},
    {"name": "Bouillabaisse", "country": "France", "ingredients": ["fish", "seafood", "saffron", "fennel"], "instructions": "Traditional fish stew from Marseille"},
    {"name": "Crème Brûlée", "country": "France", "ingredients": ["cream", "eggs", "sugar", "vanilla"], "instructions": "Custard dessert with caramelized sugar top"},
    
    # Japan (5 dishes)
    {"name": "Sushi", "country": "Japan", "ingredients": ["sushi rice", "nori", "fish", "wasabi"], "instructions": "Form rice with fish and seaweed"},
    {"name": "Ramen", "country": "Japan", "ingredients": ["ramen noodles", "broth", "egg", "pork", "green onions"], "instructions": "Serve noodles in hot broth with toppings"},
    {"name": "Tempura", "country": "Japan", "ingredients": ["shrimp", "vegetables", "tempura batter", "oil"], "instructions": "Deep fry battered ingredients until crispy"},
    {"name": "Yakitori", "country": "Japan", "ingredients": ["chicken", "tare sauce", "skewers"], "instructions": "Grill skewered chicken with sweet sauce"},
    {"name": "Miso Soup", "country": "Japan", "ingredients": ["miso paste", "dashi", "tofu", "seaweed"], "instructions": "Dissolve miso in hot dashi broth"},
    
    # India (5 dishes)
    {"name": "Butter Chicken", "country": "India", "ingredients": ["chicken", "tomato sauce", "cream", "spices"], "instructions": "Cook chicken in creamy tomato sauce"},
    {"name": "Biryani", "country": "India", "ingredients": ["basmati rice", "meat", "saffron", "spices"], "instructions": "Layer spiced rice with meat and cook"},
    {"name": "Masala Dosa", "country": "India", "ingredients": ["rice batter", "potato filling", "coconut chutney"], "instructions": "Make crepe with rice batter, fill with spiced potatoes"},
    {"name": "Tandoori Chicken", "country": "India", "ingredients": ["chicken", "yogurt", "tandoori spices"], "instructions": "Marinate chicken in spiced yogurt, grill in tandoor"},
    {"name": "Dal Makhani", "country": "India", "ingredients": ["black lentils", "butter", "cream", "spices"], "instructions": "Slow cook lentils with butter and cream"},
    
    # Mexico (5 dishes)
    {"name": "Tacos al Pastor", "country": "Mexico", "ingredients": ["pork", "pineapple", "tortillas", "onion", "cilantro"], "instructions": "Serve marinated pork on tortillas with toppings"},
    {"name": "Guacamole", "country": "Mexico", "ingredients": ["avocados", "lime", "onion", "cilantro", "chili"], "instructions": "Mash avocados with seasonings"},
    {"name": "Chiles Rellenos", "country": "Mexico", "ingredients": ["poblano peppers", "cheese", "egg batter"], "instructions": "Stuff peppers with cheese, batter and fry"},
    {"name": "Mole Poblano", "country": "Mexico", "ingredients": ["chili peppers", "chocolate", "spices", "chicken"], "instructions": "Complex sauce with chocolate and chilies served with meat"},
    {"name": "Pozole", "country": "Mexico", "ingredients": ["hominy", "pork", "red chilies", "garnishes"], "instructions": "Traditional soup with hominy and meat"},
    
    # China (5 dishes)
    {"name": "Kung Pao Chicken", "country": "China", "ingredients": ["chicken", "peanuts", "vegetables", "chili sauce"], "instructions": "Stir-fry chicken with peanuts and spicy sauce"},
    {"name": "Peking Duck", "country": "China", "ingredients": ["duck", "pancakes", "scallions", "hoisin sauce"], "instructions": "Roast duck served with pancakes and sauce"},
    {"name": "Mapo Tofu", "country": "China", "ingredients": ["tofu", "ground pork", "fermented bean paste"], "instructions": "Spicy Sichuan dish with soft tofu"},
    {"name": "Dim Sum", "country": "China", "ingredients": ["dumpling wrappers", "various fillings", "bamboo steamers"], "instructions": "Steam small portions of various foods"},
    {"name": "Hot Pot", "country": "China", "ingredients": ["broth", "raw ingredients", "dipping sauces"], "instructions": "Cook raw ingredients in shared pot of simmering broth"},
    
    # Thailand (5 dishes)
    {"name": "Pad Thai", "country": "Thailand", "ingredients": ["rice noodles", "shrimp", "tofu", "tamarind sauce"], "instructions": "Stir-fry noodles with protein and sweet-sour sauce"},
    {"name": "Tom Yum Goong", "country": "Thailand", "ingredients": ["shrimp", "lemongrass", "lime leaves", "chili"], "instructions": "Spicy and sour soup with shrimp"},
    {"name": "Green Curry", "country": "Thailand", "ingredients": ["green curry paste", "coconut milk", "chicken", "basil"], "instructions": "Cook curry paste with coconut milk and meat"},
    {"name": "Som Tam", "country": "Thailand", "ingredients": ["green papaya", "tomatoes", "fish sauce", "lime"], "instructions": "Spicy papaya salad with Thai flavors"},
    {"name": "Mango Sticky Rice", "country": "Thailand", "ingredients": ["sticky rice", "coconut milk", "mango", "sugar"], "instructions": "Sweet dessert with rice and fresh mango"},
    
    # Spain (5 dishes)
    {"name": "Paella", "country": "Spain", "ingredients": ["bomba rice", "saffron", "seafood", "vegetables"], "instructions": "Cook rice with saffron and various ingredients"},
    {"name": "Gazpacho", "country": "Spain", "ingredients": ["tomatoes", "cucumber", "peppers", "olive oil"], "instructions": "Cold soup made from fresh vegetables"},
    {"name": "Tortilla Española", "country": "Spain", "ingredients": ["eggs", "potatoes", "onions", "olive oil"], "instructions": "Spanish potato omelet cooked slowly"},
    {"name": "Jamón Ibérico", "country": "Spain", "ingredients": ["cured ham", "bread", "tomato"], "instructions": "Thinly sliced cured ham served simply"},
    {"name": "Churros", "country": "Spain", "ingredients": ["flour", "water", "oil", "sugar", "chocolate"], "instructions": "Fried dough sticks dusted with sugar"},
    
    # Greece (5 dishes)
    {"name": "Moussaka", "country": "Greece", "ingredients": ["eggplant", "ground meat", "béchamel sauce"], "instructions": "Layered casserole with eggplant and meat"},
    {"name": "Greek Salad", "country": "Greece", "ingredients": ["tomatoes", "cucumber", "feta", "olives", "olive oil"], "instructions": "Fresh salad with feta cheese and olives"},
    {"name": "Souvlaki", "country": "Greece", "ingredients": ["pork", "olive oil", "lemon", "herbs", "pita"], "instructions": "Grilled meat skewers served with pita"},
    {"name": "Spanakopita", "country": "Greece", "ingredients": ["spinach", "feta", "phyllo pastry", "herbs"], "instructions": "Spinach and feta pie in flaky pastry"},
    {"name": "Baklava", "country": "Greece", "ingredients": ["phyllo pastry", "nuts", "honey", "cinnamon"], "instructions": "Sweet layered pastry with nuts and honey"},
    
    # Turkey (5 dishes)
    {"name": "Kebab", "country": "Turkey", "ingredients": ["lamb", "vegetables", "spices", "yogurt"], "instructions": "Grilled meat served with accompaniments"},
    {"name": "Turkish Baklava", "country": "Turkey", "ingredients": ["phyllo dough", "pistachios", "honey syrup"], "instructions": "Layered pastry with nuts and sweet syrup"},
    {"name": "Turkish Delight", "country": "Turkey", "ingredients": ["sugar", "starch", "flavorings", "powdered sugar"], "instructions": "Soft confection dusted with sugar"},
    {"name": "Dolma", "country": "Turkey", "ingredients": ["grape leaves", "rice", "herbs", "pine nuts"], "instructions": "Stuffed grape leaves with seasoned rice"},
    {"name": "Pide", "country": "Turkey", "ingredients": ["bread dough", "cheese", "meat", "egg"], "instructions": "Turkish flatbread with various toppings"},
    
    # Morocco (5 dishes)
    {"name": "Tagine", "country": "Morocco", "ingredients": ["lamb", "vegetables", "preserved lemons", "spices"], "instructions": "Slow-cooked stew in cone-shaped pot"},
    {"name": "Couscous", "country": "Morocco", "ingredients": ["couscous", "vegetables", "meat", "broth"], "instructions": "Steamed semolina with stew"},
    {"name": "Pastilla", "country": "Morocco", "ingredients": ["phyllo pastry", "pigeon", "almonds", "cinnamon"], "instructions": "Sweet and savory pie with meat and nuts"},
    {"name": "Harira", "country": "Morocco", "ingredients": ["lentils", "tomatoes", "herbs", "spices"], "instructions": "Traditional soup often served during Ramadan"},
    {"name": "Mint Tea", "country": "Morocco", "ingredients": ["green tea", "fresh mint", "sugar"], "instructions": "Sweet mint tea served in traditional glasses"},
    
    # Brazil (5 dishes)
    {"name": "Feijoada", "country": "Brazil", "ingredients": ["black beans", "pork", "sausage", "beef"], "instructions": "Hearty stew with beans and various meats"},
    {"name": "Caipirinha", "country": "Brazil", "ingredients": ["cachaça", "lime", "sugar", "ice"], "instructions": "National cocktail with sugarcane spirit"},
    {"name": "Pão de Açúcar", "country": "Brazil", "ingredients": ["cassava flour", "cheese", "eggs", "milk"], "instructions": "Cheese bread rolls popular throughout Brazil"},
    {"name": "Moqueca", "country": "Brazil", "ingredients": ["fish", "coconut milk", "dendê oil", "peppers"], "instructions": "Seafood stew with coconut and palm oil"},
    {"name": "Brigadeiros", "country": "Brazil", "ingredients": ["condensed milk", "cocoa powder", "butter", "chocolate sprinkles"], "instructions": "Sweet chocolate truffles rolled in sprinkles"},
    
    # Argentina (5 dishes)
    {"name": "Asado", "country": "Argentina", "ingredients": ["beef", "salt", "chimichurri sauce"], "instructions": "Grilled meat cooked over open fire"},
    {"name": "Empanadas", "country": "Argentina", "ingredients": ["pastry dough", "beef", "onions", "spices"], "instructions": "Baked pastries filled with meat mixture"},
    {"name": "Milanesa", "country": "Argentina", "ingredients": ["beef", "breadcrumbs", "eggs", "potatoes"], "instructions": "Breaded and fried cutlet served with sides"},
    {"name": "Dulce de Leche", "country": "Argentina", "ingredients": ["milk", "sugar", "vanilla"], "instructions": "Sweet caramel-like spread made from milk"},
    {"name": "Chimichurri", "country": "Argentina", "ingredients": ["parsley", "oregano", "garlic", "oil", "vinegar"], "instructions": "Green herb sauce for grilled meats"},
    
    # Peru (5 dishes)
    {"name": "Ceviche", "country": "Peru", "ingredients": ["raw fish", "lime juice", "onions", "chili peppers"], "instructions": "Fish cured in citric acid from lime juice"},
    {"name": "Lomo Saltado", "country": "Peru", "ingredients": ["beef", "onions", "tomatoes", "french fries"], "instructions": "Stir-fried beef with vegetables and fries"},
    {"name": "Ají de Gallina", "country": "Peru", "ingredients": ["chicken", "ají peppers", "bread", "milk"], "instructions": "Creamy chicken stew with yellow peppers"},
    {"name": "Anticuchos", "country": "Peru", "ingredients": ["beef heart", "ají panca", "vinegar", "spices"], "instructions": "Grilled marinated beef heart skewers"},
    {"name": "Pisco Sour", "country": "Peru", "ingredients": ["pisco", "lime juice", "sugar", "egg white"], "instructions": "National cocktail with grape brandy"},
    
    # South Korea (5 dishes)
    {"name": "Kimchi", "country": "South Korea", "ingredients": ["napa cabbage", "chili flakes", "garlic", "ginger"], "instructions": "Fermented spicy cabbage side dish"},
    {"name": "Bulgogi", "country": "South Korea", "ingredients": ["marinated beef", "soy sauce", "pear", "sesame oil"], "instructions": "Sweet marinated grilled beef"},
    {"name": "Bibimbap", "country": "South Korea", "ingredients": ["rice", "vegetables", "meat", "gochujang"], "instructions": "Mixed rice bowl with various toppings"},
    {"name": "Korean BBQ", "country": "South Korea", "ingredients": ["various meats", "lettuce", "ssamjang", "banchan"], "instructions": "Grilled meat eaten with lettuce wraps"},
    {"name": "Tteokbokki", "country": "South Korea", "ingredients": ["rice cakes", "gochujang", "fish cake", "scallions"], "instructions": "Spicy stir-fried rice cakes"},
    
    # Lebanon (5 dishes)
    {"name": "Hummus", "country": "Lebanon", "ingredients": ["chickpeas", "tahini", "lemon juice", "garlic"], "instructions": "Creamy chickpea dip with tahini"},
    {"name": "Tabbouleh", "country": "Lebanon", "ingredients": ["bulgur", "parsley", "tomatoes", "lemon", "olive oil"], "instructions": "Fresh parsley salad with bulgur"},
    {"name": "Fattoush", "country": "Lebanon", "ingredients": ["mixed greens", "vegetables", "pita chips", "sumac"], "instructions": "Mixed salad with toasted pita bread"},
    {"name": "Kibbeh", "country": "Lebanon", "ingredients": ["bulgur", "ground meat", "onions", "spices"], "instructions": "Fried bulgur and meat croquettes"},
    {"name": "Manakish", "country": "Lebanon", "ingredients": ["flatbread", "za'atar", "olive oil", "cheese"], "instructions": "Baked flatbread with herbs and cheese"},
    
    # Russia (5 dishes)
    {"name": "Borscht", "country": "Russia", "ingredients": ["beets", "cabbage", "carrots", "sour cream"], "instructions": "Beet soup served hot or cold"},
    {"name": "Beef Stroganoff", "country": "Russia", "ingredients": ["beef", "mushrooms", "sour cream", "onions"], "instructions": "Creamy beef dish with mushrooms"},
    {"name": "Pelmeni", "country": "Russia", "ingredients": ["dumpling dough", "ground meat", "onions"], "instructions": "Small dumplings filled with meat"},
    {"name": "Blini", "country": "Russia", "ingredients": ["flour", "eggs", "milk", "various fillings"], "instructions": "Thin pancakes served with sweet or savory fillings"},
    {"name": "Caviar", "country": "Russia", "ingredients": ["fish roe", "blini", "sour cream", "chives"], "instructions": "Luxury fish eggs served on pancakes"},
    
    # Ethiopia (5 dishes)
    {"name": "Injera", "country": "Ethiopia", "ingredients": ["teff flour", "water", "fermentation"], "instructions": "Spongy sourdough flatbread"},
    {"name": "Doro Wat", "country": "Ethiopia", "ingredients": ["chicken", "berbere spice", "hard-boiled eggs"], "instructions": "Spicy chicken stew with eggs"},
    {"name": "Kitfo", "country": "Ethiopia", "ingredients": ["raw minced beef", "mitmita spice", "clarified butter"], "instructions": "Ethiopian steak tartare with spices"},
    {"name": "Berbere", "country": "Ethiopia", "ingredients": ["chili peppers", "garlic", "ginger", "various spices"], "instructions": "Complex spice blend used in many dishes"},
    {"name": "Ethiopian Coffee", "country": "Ethiopia", "ingredients": ["coffee beans", "water", "traditional ceremony"], "instructions": "Coffee prepared in traditional ceremony"},
    
    # Nigeria (5 dishes)
    {"name": "Jollof Rice", "country": "Nigeria", "ingredients": ["rice", "tomatoes", "peppers", "spices"], "instructions": "One-pot rice dish with tomato base"},
    {"name": "Suya", "country": "Nigeria", "ingredients": ["beef", "suya spice", "onions", "tomatoes"], "instructions": "Spiced grilled meat skewers"},
    {"name": "Egusi Soup", "country": "Nigeria", "ingredients": ["melon seeds", "leafy vegetables", "meat", "fish"], "instructions": "Thick soup made with ground melon seeds"},
    {"name": "Pounded Yam", "country": "Nigeria", "ingredients": ["yam", "water", "mortar and pestle"], "instructions": "Smooth starchy side dish made from yam"},
    {"name": "Chin Chin", "country": "Nigeria", "ingredients": ["flour", "sugar", "butter", "milk", "oil"], "instructions": "Sweet fried pastry cubes"},

    # USA (5 dishes)
    {"name": "Hamburger", "country": "USA", "ingredients": ["ground beef", "burger buns", "lettuce", "tomato", "cheese"], "instructions": "Grill beef patty, assemble burger with toppings"},
    {"name": "BBQ Ribs", "country": "USA", "ingredients": ["pork ribs", "BBQ sauce", "dry rub spices", "coleslaw"], "instructions": "Slow smoke ribs with dry rub, glaze with BBQ sauce"},
    {"name": "Mac and Cheese", "country": "USA", "ingredients": ["macaroni pasta", "cheddar cheese", "milk", "butter", "breadcrumbs"], "instructions": "Cook pasta, make cheese sauce, combine and bake"},
    {"name": "Apple Pie", "country": "USA", "ingredients": ["apples", "pie crust", "cinnamon", "sugar", "butter"], "instructions": "Fill crust with spiced apples, cover and bake"},
    {"name": "Buffalo Wings", "country": "USA", "ingredients": ["chicken wings", "hot sauce", "butter", "celery", "blue cheese"], "instructions": "Fry wings, toss in buffalo sauce, serve with celery and dip"},

    # United Kingdom (5 dishes)
    {"name": "Fish and Chips", "country": "United Kingdom", "ingredients": ["white fish", "potatoes", "batter", "mushy peas", "malt vinegar"], "instructions": "Batter and fry fish, serve with thick-cut chips"},
    {"name": "Shepherd's Pie", "country": "United Kingdom", "ingredients": ["ground lamb", "vegetables", "mashed potatoes", "gravy"], "instructions": "Layer meat and vegetables, top with mashed potatoes and bake"},
    {"name": "Bangers and Mash", "country": "United Kingdom", "ingredients": ["sausages", "mashed potatoes", "onion gravy", "peas"], "instructions": "Grill sausages, serve with mashed potatoes and gravy"},
    {"name": "Afternoon Tea", "country": "United Kingdom", "ingredients": ["tea", "scones", "clotted cream", "jam", "finger sandwiches"], "instructions": "Serve traditional tea service with scones and sandwiches"},
    {"name": "Roast Beef", "country": "United Kingdom", "ingredients": ["beef roast", "Yorkshire pudding", "roasted vegetables", "gravy"], "instructions": "Roast beef with traditional accompaniments"},

    # Germany (5 dishes)
    {"name": "Bratwurst", "country": "Germany", "ingredients": ["bratwurst sausage", "sauerkraut", "mustard", "beer", "bread"], "instructions": "Grill bratwurst, serve with sauerkraut and mustard"},
    {"name": "Sauerbraten", "country": "Germany", "ingredients": ["beef roast", "red wine vinegar", "vegetables", "gingersnaps", "red cabbage"], "instructions": "Marinate beef for days, braise and serve with sweet-sour sauce"},
    {"name": "Pretzel", "country": "Germany", "ingredients": ["bread dough", "coarse salt", "lye solution", "butter"], "instructions": "Shape dough, dip in lye, sprinkle with salt and bake"},
    {"name": "Schnitzel", "country": "Germany", "ingredients": ["pork or veal", "breadcrumbs", "eggs", "lemon", "potato salad"], "instructions": "Bread and fry cutlet until golden, serve with lemon"},
    {"name": "Black Forest Cake", "country": "Germany", "ingredients": ["chocolate cake", "cherries", "whipped cream", "kirsch", "chocolate shavings"], "instructions": "Layer chocolate cake with cherries and cream"},

    # Canada (5 dishes)
    {"name": "Poutine", "country": "Canada", "ingredients": ["french fries", "cheese curds", "gravy", "green onions"], "instructions": "Top hot fries with cheese curds and gravy"},
    {"name": "Maple Syrup Pancakes", "country": "Canada", "ingredients": ["pancakes", "pure maple syrup", "butter", "bacon", "berries"], "instructions": "Stack fluffy pancakes, drizzle with real maple syrup"},
    {"name": "Tourtière", "country": "Canada", "ingredients": ["ground pork", "pie crust", "potatoes", "spices", "cranberry sauce"], "instructions": "Traditional meat pie baked until golden"},
    {"name": "Butter Tarts", "country": "Canada", "ingredients": ["tart shells", "butter", "brown sugar", "eggs", "raisins"], "instructions": "Fill tart shells with sweet butter mixture and bake"},
    {"name": "Montreal Bagels", "country": "Canada", "ingredients": ["bagel dough", "sesame seeds", "poppy seeds", "cream cheese", "smoked salmon"], "instructions": "Boil then bake bagels, serve with cream cheese and salmon"},

    # Australia (5 dishes)
    {"name": "Meat Pie", "country": "Australia", "ingredients": ["ground beef", "pie pastry", "onions", "gravy", "tomato sauce"], "instructions": "Fill pastry with seasoned meat, bake until golden"},
    {"name": "Lamingtons", "country": "Australia", "ingredients": ["sponge cake", "chocolate icing", "coconut flakes", "jam", "cream"], "instructions": "Coat cake squares in chocolate and coconut"},
    {"name": "Vegemite Toast", "country": "Australia", "ingredients": ["bread", "butter", "vegemite", "cheese"], "instructions": "Toast bread, spread with butter and thin layer of vegemite"},
    {"name": "Barbie Prawns", "country": "Australia", "ingredients": ["prawns", "garlic", "lemon", "herbs", "beer"], "instructions": "Grill prawns on the barbecue with garlic and herbs"},
    {"name": "Pavlova", "country": "Australia", "ingredients": ["meringue", "whipped cream", "fresh fruits", "passion fruit", "berry coulis"], "instructions": "Top crispy meringue base with cream and fresh fruits"},
]

# Utility functions
def get_countries():
    """Get list of all countries in seed data"""
    return sorted(list(set(dish['country'] for dish in GEODISH_SEED_DATA)))

def get_dishes_by_country(country):
    """Get all dishes for a specific country"""
    return [dish for dish in GEODISH_SEED_DATA if dish['country'] == country]

def get_dish_count():
    """Get total number of dishes"""
    return len(GEODISH_SEED_DATA)

def get_country_count():
    """Get total number of countries"""
    return len(get_countries())
