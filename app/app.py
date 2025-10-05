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

# Initialize database and seed manager.
db = Database()
seed_manager = SeedManager(db)

# All your existing routes stay the same...
# (I'll just show the updated seed routes)

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
@app.route('/user/<userid>/recipes/<recipeid>', methods=['PUT'])
def update_user_recipe(userid, recipeid):
    data = request.get_json()
    updated = db.update_user_recipe(userid, recipeid, data)
    if updated:
        return jsonify({"message": "Recipe updated"}), 200
    else:
        return jsonify({"error": "Recipe not found"}), 404

# Add this to your app.py to fix /seed-info endpoint
def get_countries():
    """Get list of available countries"""
    return ['Italy', 'France', 'Spain', 'Germany', 'Greece']  # Your countries list

# ... rest of your routes stay exactly the same
