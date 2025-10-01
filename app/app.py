from flask import Flask, request, jsonify
from flask_cors import CORS
from app.models import Database
from app.config import Config
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

# Initialize database
db = Database()

# CRUD Operations for Dishes (following person/{id} pattern)
@app.route('/dish/<dish_id>', methods=['POST'])
def create_dish(dish_id):
    """Create a new dish with specified ID"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON body required"}), 400
        
        # Add the custom dish_id to the data
        data['custom_id'] = dish_id
        result_id = db.create_dish(data)
        
        logger.info(f"Dish created with ID: {result_id}")
        return jsonify({
            "message": "Dish created successfully",
            "id": result_id
        }), 201
    except Exception as e:
        logger.error(f"Error creating dish: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/dish/<dish_id>', methods=['GET'])
def get_dish(dish_id):
    """Get specific dish by ID"""
    try:
        dish = db.get_dish_by_id(dish_id)
        if dish:
            logger.info(f"Retrieved dish: {dish['name']}")
            return jsonify(dish), 200
        return jsonify({"error": "Dish not found"}), 404
    except Exception as e:
        logger.error(f"Error getting dish: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/dish/<dish_id>', methods=['PUT'])
def update_dish(dish_id):
    """Update existing dish"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON body required"}), 400
        
        success = db.update_dish(dish_id, data)
        if success:
            logger.info(f"Dish {dish_id} updated successfully")
            return jsonify({"message": "Dish updated successfully"}), 200
        return jsonify({"error": "Dish not found"}), 404
    except Exception as e:
        logger.error(f"Error updating dish: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/dish/<dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    """Delete dish by ID"""
    try:
        success = db.delete_dish(dish_id)
        if success:
            logger.info(f"Dish {dish_id} deleted successfully")
            return jsonify({"message": "Dish deleted successfully"}), 200
        return jsonify({"error": "Dish not found"}), 404
    except Exception as e:
        logger.error(f"Error deleting dish: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/dish', methods=['GET'])
def get_all_dish_ids():
    """Get array of all dish IDs"""
    try:
        dish_ids = db.get_all_dish_ids()
        logger.info(f"Retrieved {len(dish_ids)} dish IDs")
        return jsonify(dish_ids), 200
    except Exception as e:
        logger.error(f"Error getting dish IDs: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Additional GeoDish specific endpoints
@app.route('/countries', methods=['GET'])
def get_countries():
    """Get list of all available countries"""
    try:
        countries = db.get_countries()
        logger.info(f"Retrieved {len(countries)} countries")
        return jsonify({"countries": countries}), 200
    except Exception as e:
        logger.error(f"Error getting countries: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/dish/random/<country>', methods=['GET'])
def get_random_dish(country):
    """Get a random dish from specified country"""
    try:
        dish = db.get_random_dish_by_country(country)
        if dish:
            logger.info(f"Retrieved random dish from {country}: {dish['name']}")
            return jsonify(dish), 200
        return jsonify({"error": "No dishes found for this country"}), 404
    except Exception as e:
        logger.error(f"Error getting random dish: {str(e)}")
        return jsonify({"error": str(e)}), 500

# User recipe management
@app.route('/user/<user_id>/recipes', methods=['POST'])
def save_recipe(user_id):
    """Save a dish to user's recipes"""
    try:
        data = request.get_json()
        dish_id = data.get('dish_id')
        custom_name = data.get('custom_name')
        
        if not dish_id:
            return jsonify({"error": "dish_id is required"}), 400
        
        result = db.save_dish_to_user_recipes(user_id, dish_id, custom_name)
        if result:
            logger.info(f"User {user_id} saved dish {dish_id}")
            return jsonify({
                "message": "Recipe saved successfully",
                "recipe_id": result
            }), 201
        return jsonify({"error": "Recipe already saved or dish not found"}), 400
    except Exception as e:
        logger.error(f"Error saving recipe: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/user/<user_id>/recipes', methods=['GET'])
def get_user_recipe_ids(user_id):
    """Get array of user's saved recipe IDs"""
    try:
        recipe_ids = db.get_user_recipe_ids(user_id)
        logger.info(f"Retrieved {len(recipe_ids)} recipe IDs for user {user_id}")
        return jsonify(recipe_ids), 200
    except Exception as e:
        logger.error(f"Error getting user recipe IDs: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/user/<user_id>/recipes/full', methods=['GET'])
def get_user_recipes_full(user_id):
    """Get full recipe objects for user (for UI)"""
    try:
        recipes = db.get_user_recipes(user_id)
        logger.info(f"Retrieved {len(recipes)} full recipes for user {user_id}")
        return jsonify({"recipes": recipes}), 200
    except Exception as e:
        logger.error(f"Error getting user recipes: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/user/<user_id>/recipes/<recipe_id>', methods=['DELETE'])
def delete_recipe(user_id, recipe_id):
    """Delete a saved recipe"""
    try:
        success = db.delete_user_recipe(user_id, recipe_id)
        if success:
            logger.info(f"User {user_id} deleted recipe {recipe_id}")
            return jsonify({"message": "Recipe deleted successfully"}), 200
        return jsonify({"error": "Recipe not found"}), 404
    except Exception as e:
        logger.error(f"Error deleting recipe: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/seed', methods=['POST'])
def seed_database():
    """Seed database with sample dishes"""
    try:
        result = db.seed_dishes()
        return jsonify({"message": result}), 200
    except Exception as e:
        logger.error(f"Error seeding database: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/metrics', methods=['GET'])
def metrics():
    """Health check and metrics"""
    try:
        countries = db.get_countries()
        total_dishes = db.get_total_dish_count()
        return jsonify({
            "status": "healthy",
            "total_countries": len(countries),
            "total_dishes": total_dishes,
            "available_countries": countries
        }), 200
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    """Serve main page"""
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
