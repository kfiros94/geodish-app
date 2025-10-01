from pymongo import MongoClient
from bson import ObjectId
import os
import random

class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://mongodb:27017/'))
        self.db = self.client.geodish
        self.dishes = self.db.dishes
        self.users = self.db.users
        self.user_recipes = self.db.user_recipes

    # Country and Dish operations
    def get_countries(self):
        """Get list of all available countries"""
        countries = self.dishes.distinct("country")
        return sorted(countries)

    def get_random_dish_by_country(self, country):
        """Get a random dish from a specific country"""
        pipeline = [
            {"$match": {"country": country}},
            {"$sample": {"size": 1}}
        ]
        result = list(self.dishes.aggregate(pipeline))
        if result:
            result[0]['_id'] = str(result[0]['_id'])
            return result[0]
        return None

    def get_dish_by_id(self, dish_id):
        """Get a specific dish by ID"""
        dish = self.dishes.find_one({"_id": ObjectId(dish_id)})
        if dish:
            dish['_id'] = str(dish['_id'])
        return dish

    def get_dishes_by_country(self, country):
        """Get all dishes from a specific country"""
        dishes = list(self.dishes.find({"country": country}))
        for dish in dishes:
            dish['_id'] = str(dish['_id'])
        return dishes

    # User Recipe operations
    def save_dish_to_user_recipes(self, user_id, dish_id, custom_name=None):
        """Save a dish to user's personal recipes"""
        dish = self.get_dish_by_id(dish_id)
        if not dish:
            return False
        
        recipe_data = {
            "user_id": user_id,
            "dish_id": dish_id,
            "dish_name": dish['name'],
            "country": dish['country'],
            "custom_name": custom_name or dish['name'],
            "ingredients": dish.get('ingredients', []),
            "instructions": dish.get('instructions', ''),
            "saved_at": str(ObjectId())
        }
        
        # Check if already saved
        existing = self.user_recipes.find_one({
            "user_id": user_id, 
            "dish_id": dish_id
        })
        
        if existing:
            return False
        
        result = self.user_recipes.insert_one(recipe_data)
        return str(result.inserted_id)

    def get_user_recipes(self, user_id):
        """Get all saved recipes for a user"""
        recipes = list(self.user_recipes.find({"user_id": user_id}))
        for recipe in recipes:
            recipe['_id'] = str(recipe['_id'])
        return recipes

    def delete_user_recipe(self, user_id, recipe_id):
        """Remove a recipe from user's saved recipes"""
        result = self.user_recipes.delete_one({
            "_id": ObjectId(recipe_id),
            "user_id": user_id
        })      
        return result.deleted_count > 0

    def create_dish(self, dish_data):
        """Create a new dish"""
        result = self.dishes.insert_one(dish_data)
        return str(result.inserted_id)

    def update_dish(self, dish_id, update_data):
        """Update an existing dish"""
        result = self.dishes.update_one(
            {"_id": ObjectId(dish_id)}, 
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_dish(self, dish_id):
        """Delete a dish"""
        result = self.dishes.delete_one({"_id": ObjectId(dish_id)})
        return result.deleted_count > 0

    def get_all_dish_ids(self):
        """Get array of all dish IDs"""
        dishes = list(self.dishes.find({}, {"_id": 1}))
        return [str(dish['_id']) for dish in dishes]

    def get_user_recipe_ids(self, user_id):
        """Get array of user's recipe IDs only"""
        recipes = list(self.user_recipes.find({"user_id": user_id}, {"_id": 1}))
        return [str(recipe['_id']) for recipe in recipes]

    def get_total_dish_count(self):
        """Get total number of dishes"""
        return self.dishes.count_documents({})

    def seed_dishes(self):
        """Seed the database with sample dishes from 20 countries"""
        if self.dishes.count_documents({}) > 0:
            return "Database already seeded"
        # ... rest of your existing code

        
        sample_dishes = self._get_sample_dishes()
        self.dishes.insert_many(sample_dishes)
        return f"Seeded {len(sample_dishes)} dishes from 20 countries"

    def _get_sample_dishes(self):
        """Sample dishes data for 20 countries, 5 dishes each"""
        return [
            # Italy
            {"name": "Spaghetti Carbonara", "country": "Italy", "ingredients": ["spaghetti", "eggs", "bacon", "parmesan", "black pepper"], "instructions": "Cook pasta, mix with egg and cheese mixture"},
            {"name": "Margherita Pizza", "country": "Italy", "ingredients": ["pizza dough", "tomato sauce", "mozzarella", "basil"], "instructions": "Top dough with sauce, cheese, and basil, then bake"},
            {"name": "Risotto Milanese", "country": "Italy", "ingredients": ["arborio rice", "saffron", "onion", "white wine", "parmesan"], "instructions": "Slowly cook rice with saffron and stock"},
            {"name": "Tiramisu", "country": "Italy", "ingredients": ["ladyfingers", "coffee", "mascarpone", "cocoa powder"], "instructions": "Layer coffee-soaked cookies with mascarpone cream"},
            {"name": "Osso Buco", "country": "Italy", "ingredients": ["veal shanks", "tomatoes", "wine", "vegetables"], "instructions": "Braise veal shanks with vegetables and wine"},
            
            # Japan
            {"name": "Sushi", "country": "Japan", "ingredients": ["sushi rice", "nori", "fish", "wasabi"], "instructions": "Form rice with fish and seaweed"},
            {"name": "Ramen", "country": "Japan", "ingredients": ["ramen noodles", "broth", "egg", "pork", "green onions"], "instructions": "Serve noodles in hot broth with toppings"},
            {"name": "Tempura", "country": "Japan", "ingredients": ["shrimp", "vegetables", "tempura batter", "oil"], "instructions": "Deep fry battered ingredients until crispy"},
            {"name": "Yakitori", "country": "Japan", "ingredients": ["chicken", "tare sauce", "skewers"], "instructions": "Grill skewered chicken with sweet sauce"},
            {"name": "Miso Soup", "country": "Japan", "ingredients": ["miso paste", "dashi", "tofu", "seaweed"], "instructions": "Dissolve miso in hot dashi broth"},
            
            # India
            {"name": "Butter Chicken", "country": "India", "ingredients": ["chicken", "tomato sauce", "cream", "spices"], "instructions": "Cook chicken in creamy tomato sauce"},
            {"name": "Biryani", "country": "India", "ingredients": ["basmati rice", "meat", "saffron", "spices"], "instructions": "Layer spiced rice with meat and cook"},
            {"name": "Masala Dosa", "country": "India", "ingredients": ["rice batter", "potato filling", "coconut chutney"], "instructions": "Make crepe with rice batter, fill with spiced potatoes"},
            {"name": "Tandoori Chicken", "country": "India", "ingredients": ["chicken", "yogurt", "tandoori spices"], "instructions": "Marinate chicken in spiced yogurt, grill in tandoor"},
            {"name": "Dal Makhani", "country": "India", "ingredients": ["black lentils", "butter", "cream", "spices"], "instructions": "Slow cook lentils with butter and cream"},
            
            # Mexico
            {"name": "Tacos al Pastor", "country": "Mexico", "ingredients": ["pork", "pineapple", "tortillas", "onion", "cilantro"], "instructions": "Serve marinated pork on tortillas with toppings"},
            {"name": "Guacamole", "country": "Mexico", "ingredients": ["avocados", "lime", "onion", "cilantro", "chili"], "instructions": "Mash avocados with seasonings"},
            {"name": "Chiles Rellenos", "country": "Mexico", "ingredients": ["poblano peppers", "cheese", "egg batter"], "instructions": "Stuff peppers with cheese, batter and fry"},
            {"name": "Mole Poblano", "country": "Mexico", "ingredients": ["chili peppers", "chocolate", "spices", "chicken"], "instructions": "Complex sauce with chocolate and chilies served with meat"},
            {"name": "Pozole", "country": "Mexico", "ingredients": ["hominy", "pork", "red chilies", "garnishes"], "instructions": "Traditional soup with hominy and meat"},
            
            # France
            {"name": "Coq au Vin", "country": "France", "ingredients": ["chicken", "red wine", "mushrooms", "bacon"], "instructions": "Braise chicken in red wine with vegetables"},
            {"name": "Ratatouille", "country": "France", "ingredients": ["eggplant", "zucchini", "tomatoes", "herbs"], "instructions": "Stew Mediterranean vegetables together"},
            {"name": "Croissant", "country": "France", "ingredients": ["puff pastry", "butter"], "instructions": "Layer butter in dough, roll and bake"},
            {"name": "Bouillabaisse", "country": "France", "ingredients": ["fish", "seafood", "saffron", "fennel"], "instructions": "Traditional fish stew from Marseille"},
            {"name": "Crème Brûlée", "country": "France", "ingredients": ["cream", "eggs", "sugar", "vanilla"], "instructions": "Custard dessert with caramelized sugar top"},
        ]
# Note: Add more countries and dishes as needed to reach 20 countries with 5 dishes each.