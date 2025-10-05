"""
GeoDish Seed Manager
Handles all seeding operations
"""
from .data import GEODISH_SEED_DATA, get_country_count, get_dish_count, get_countries  # Add get_countries here
import logging
logger = logging.getLogger(__name__)

class SeedManager:
    def __init__(self, db):
        self.db = db
        
    def is_database_seeded(self):
        """Check if database already contains data"""
        return self.db.dishes.count_documents({}) > 0
        
    def seed_database(self, force=False):
        """Seed database with complete data"""
        if not force and self.is_database_seeded():
            countries = len(self.db.get_countries())
            dishes = self.db.dishes.count_documents({})
            return f"Database already seeded with {countries} countries and {dishes} dishes"
        
        # Clear existing data if force seeding
        if force:
            self.db.dishes.delete_many({})
            self.db.user_recipes.delete_many({})
            logger.info("Cleared existing database data for force seed")
        
        # Insert all seed data
        self.db.dishes.insert_many(GEODISH_SEED_DATA.copy())
        
        countries = get_country_count()
        dishes = get_dish_count()
        
        logger.info(f"Successfully seeded database with {countries} countries and {dishes} dishes")
        return f"Successfully seeded {dishes} dishes from {countries} countries"
        
    def get_seed_statistics(self):
        """Get statistics about seed data"""
        return {
            "total_countries": get_country_count(),
            "total_dishes": get_dish_count(),
            "dishes_per_country": get_dish_count() // get_country_count(),
            "countries": get_countries()
        }
