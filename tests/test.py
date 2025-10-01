import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.app import app
from app.models import Database
import json

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def db():
    """Create test database instance"""
    return Database()

def test_countries_endpoint(client):
    """Test countries endpoint returns list"""
    response = client.get('/countries')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'countries' in data
    assert isinstance(data['countries'], list)

def test_random_dish_endpoint(client):
    """Test random dish endpoint"""
    # First seed the database
    client.post('/seed')
    
    response = client.get('/dish/random/Italy')
    assert response.status_code in [200, 404]  # 404 if no dishes found
    
    if response.status_code == 200:
        data = json.loads(response.data)
        assert 'name' in data
        assert 'country' in data
        assert data['country'] == 'Italy'

def test_save_recipe_endpoint(client):
    """Test saving a recipe"""
    # First seed and get a dish
    client.post('/seed')
    
    # Get a random dish first
    dish_response = client.get('/dish/random/Italy')
    if dish_response.status_code == 200:
        dish_data = json.loads(dish_response.data)
        dish_id = dish_data['_id']
        
        # Save the recipe
        save_data = {'dish_id': dish_id}
        response = client.post('/user/testuser/recipes', 
                             data=json.dumps(save_data),
                             content_type='application/json')
        assert response.status_code in [201, 400]  # 400 if already saved

def test_get_user_recipes(client):
    """Test getting user recipes"""
    response = client.get('/user/testuser/recipes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'recipes' in data
    assert isinstance(data['recipes'], list)

def test_metrics_endpoint(client):
    """Test metrics endpoint"""
    response = client.get('/metrics')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'status' in data
    assert data['status'] == 'healthy'

def test_seed_endpoint(client):
    """Test database seeding"""
    response = client.post('/seed')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data

def test_static_file_serving(client):
    """Test static file serving"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'GeoDish' in response.data

if __name__ == '__main__':
    pytest.main([__file__])
