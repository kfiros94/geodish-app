from flask import Flask, request, jsonify
from flask_cors import CORS
from app.models import Database
from app.config import Config
from app.seed_manager import SeedManager
import logging
import os

# Get absolute path to static folder
current_dir = os.path.dirname(os.path.abspath(__file__))
static_folder = os.path.join(os.path.dirname(current_dir), 'static')

app = Flask(__name__, static_folder=static_folder, static_url_path='/static')
app.config.from_object(Config)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database and seed manager
db = Database()
seed_manager = SeedManager(db)

# Root route to serve HTML
@app.route('/', methods=['GET'])
def index():
    """Serve the main GeoDish application page"""
    try:
        return app.send_static_file('index.html')
    except Exception as e:
        logger.error(f"Error serving index page: {str(e)}")
        return jsonify({"error": "index.html not found"}), 500

# Countries endpoint
@app.route('/countries', methods=['GET'])
def get_countries_route():
    """Get list of all available countries"""
    try:
        countries = db.get_countries()
        logger.info(f"Found {len(countries)} countries")
        return jsonify(countries), 200
    except Exception as e:
        logger.error(f"Error getting countries: {str(e)}")
        return jsonify({"error": str(e)}), 500

# User recipes endpoint
@app.route('/user/<user_id>/recipes/full', methods=['GET'])
def get_user_recipes_full(user_id):
    """Get full details of user's recipes"""
    try:
        recipes = db.get_user_recipes(user_id)
        logger.info(f"Found {len(recipes)} recipes for user {user_id}")
        return jsonify(recipes), 200
    except Exception as e:
        logger.error(f"Error getting detailed recipes for {user_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Random dish by country
@app.route('/dish/<country>', methods=['GET'])
def get_random_dish(country):
    """Get a random dish from a specific country"""
    try:
        dish = db.get_random_dish_by_country(country)
        if dish:
            logger.info(f"Found dish: {dish['name']} from {country}")
            return jsonify(dish), 200
        else:
            return jsonify({"error": f"No dishes found for country: {country}"}), 404
    except Exception as e:
        logger.error(f"Error getting dish for {country}: {str(e)}")
        return jsonify({"error": str(e)}), 500

# MISSING ROUTE: Save dish to user's recipes (THIS WAS MISSING!)
@app.route('/user/<user_id>/save-dish', methods=['POST'])
def save_dish_to_user_recipes(user_id):
    """Save a dish to user's recipes"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'dishid' not in data:
            return jsonify({"error": "dishid is required"}), 400
            
        dish_id = data['dishid']
        custom_name = data.get('customname')
        
        # Save dish to user recipes using your existing method
        recipe_id = db.save_dish_to_user_recipes(user_id, dish_id, custom_name)
        
        if recipe_id:
            logger.info(f"Saved dish {dish_id} as recipe {recipe_id} for user {user_id}")
            return jsonify({
                "message": "Recipe saved successfully",
                "recipeId": recipe_id
            }), 201
        else:
            # Recipe already exists or dish not found
            return jsonify({"error": "Recipe already exists or dish not found"}), 409
            
    except Exception as e:
        logger.error(f"Error saving dish for {user_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

# MISSING ROUTE: Delete user's recipe (THIS WAS MISSING!)
@app.route('/user/<user_id>/recipes/<recipe_id>', methods=['DELETE'])
def delete_user_recipe_route(user_id, recipe_id):
    """Delete a user's saved recipe"""
    try:
        deleted = db.delete_user_recipe(user_id, recipe_id)
        
        if deleted:
            logger.info(f"Deleted recipe {recipe_id} for user {user_id}")
            return jsonify({"message": "Recipe deleted successfully"}), 200
        else:
            return jsonify({"error": "Recipe not found"}), 404
            
    except Exception as e:
        logger.error(f"Error deleting recipe {recipe_id} for {user_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Update user recipe
@app.route('/user/<userid>/recipes/<recipeid>', methods=['PUT'])
def update_user_recipe(userid, recipeid):
    """Update a user's recipe"""
    try:
        data = request.get_json()
        updated = db.update_user_recipe(userid, recipeid, data)
        if updated:
            return jsonify({"message": "Recipe updated"}), 200
        else:
            return jsonify({"error": "Recipe not found"}), 404
    except Exception as e:
        logger.error(f"Error updating recipe {recipeid} for {userid}: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Seed routes
@app.route('/seed', methods=['POST'])
def seed_database():
    """Seed database with sample dishes"""
    try:
        result = seed_manager.seed_database(force=False)
        return jsonify({"message": result}), 200
    except Exception as e:
        logger.error(f"Error seeding database: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/force-seed', methods=['POST'])
def force_seed_database():
    """Force seed database (clears existing data)"""
    try:
        result = seed_manager.seed_database(force=True)
        return jsonify({"message": result}), 200
    except Exception as e:
        logger.error(f"Error force seeding database: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/seed-info', methods=['GET'])
def get_seed_info():
    """Get information about seed data"""
    try:
        stats = seed_manager.get_seed_statistics()
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Error getting seed info: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Health check
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "GeoDish API is running"}), 200

# Metrics for monitoring
@app.route('/metrics', methods=['GET'])
def get_metrics():
    """Get application metrics"""
    try:
        total_dishes = db.get_total_dish_count()
        countries = db.get_countries()
        return jsonify({
            "total_dishes": total_dishes,
            "total_countries": len(countries),
            "status": "healthy"
        }), 200
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
