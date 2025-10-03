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

    def get_total_dish_count(self):
        """Get total number of dishes in database"""
        return self.dishes.count_documents({})

    # CRUD operations for dishes
    def create_dish(self, dish_data):
        """Create a new dish"""
        result = self.dishes.insert_one(dish_data)
        return str(result.inserted_id)

    def update_dish(self, dish_id, dish_data):
        """Update an existing dish"""
        result = self.dishes.update_one(
            {"_id": ObjectId(dish_id)},
            {"$set": dish_data}
        )
        return result.modified_count > 0

    def delete_dish(self, dish_id):
        """Delete a dish"""
        result = self.dishes.delete_one({"_id": ObjectId(dish_id)})
        return result.deleted_count > 0

    def get_all_dish_ids(self):
        """Get array of all dish IDs"""
        dishes = self.dishes.find({}, {"_id": 1})
        return [str(dish["_id"]) for dish in dishes]

    # User recipe operations
    def save_dish_to_user_recipes(self, user_id, dish_id, custom_name=None):
        """Save a dish to user's recipes"""
        # Check if recipe already exists
        existing = self.user_recipes.find_one({
            "user_id": user_id,
            "dish_id": dish_id
        })
        
        if existing:
            return None  # Already saved
        
        # Get the dish details
        dish = self.get_dish_by_id(dish_id)
        if not dish:
            return None  # Dish not found
        
        recipe_data = {
            "user_id": user_id,
            "dish_id": dish_id,
            "custom_name": custom_name or dish['name'],
            "original_dish": dish,
            "saved_at": None  # You might want to add timestamp
        }
        
        result = self.user_recipes.insert_one(recipe_data)
        return str(result.inserted_id)

    def get_user_recipes(self, user_id):
        """Get all saved recipes for a user"""
        recipes = list(self.user_recipes.find({"user_id": user_id}))
        for recipe in recipes:
            recipe['_id'] = str(recipe['_id'])
            if 'original_dish' in recipe and '_id' in recipe['original_dish']:
                recipe['original_dish']['_id'] = str(recipe['original_dish']['_id'])
        return recipes

    def get_user_recipe_ids(self, user_id):
        """Get array of user's saved recipe IDs"""
        recipes = self.user_recipes.find({"user_id": user_id}, {"_id": 1})
        return [str(recipe["_id"]) for recipe in recipes]

    def delete_user_recipe(self, user_id, recipe_id):
        """Delete a saved recipe"""
        result = self.user_recipes.delete_one({
            "_id": ObjectId(recipe_id),
            "user_id": user_id
        })
        return result.deleted_count > 0

    # Legacy method for backward compatibility - now uses SeedManager
    def seed_dishes(self):
        """Legacy seed method - use SeedManager instead"""
        from .seed_manager import SeedManager
        seed_manager = SeedManager(self)
        return seed_manager.seed_database()
