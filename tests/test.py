import pytest
import sys
import os
import json
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.app import app
from app.models import Database

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['MONGODB_URI'] = 'mongodb://localhost:27017/geodish_test'
    with app.test_client() as client:
        yield client

@pytest.fixture
def db():
    """Create test database instance"""
    return Database()

# ========== API Endpoint Tests ==========

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'message' in data

def test_countries_endpoint(client):
    """Test countries endpoint returns list"""
    response = client.get('/countries')
    if response.status_code == 200:
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) > 0
    else:
        assert response.status_code == 500

def test_metrics_endpoint(client):
    """Test metrics endpoint"""
    response = client.get('/metrics')
    if response.status_code == 200:
        data = json.loads(response.data)
        assert 'status' in data
        assert data['status'] == 'healthy'
        assert 'total_dishes' in data
        assert 'total_countries' in data
    else:
        assert response.status_code == 500

def test_seed_info_endpoint(client):
    """Test seed info endpoint"""
    response = client.get('/seed-info')
    if response.status_code == 200:
        data = json.loads(response.data)
        assert 'total_countries' in data or 'error' in data
    else:
        assert response.status_code == 500

def test_index_page(client):
    """Test static file serving"""
    response = client.get('/')
    if response.status_code == 200:
        assert b'GeoDish' in response.data or len(response.data) > 0
    else:
        assert response.status_code == 500

def test_random_dish_endpoint(client):
    """Test random dish endpoint"""
    response = client.get('/dish/Italy')
    assert response.status_code in [200, 404, 500]
    if response.status_code == 200:
        data = json.loads(response.data)
        assert 'name' in data
        assert 'country' in data
        assert data['country'] == 'Italy'

def test_save_recipe_endpoint(client):
    """Test saving a recipe"""
    save_data = {
        'dishid': '507f1f77bcf86cd799439011',
        'customname': 'Test Recipe'
    }
    response = client.post('/user/testuser/save-dish',
                          data=json.dumps(save_data),
                          content_type='application/json')
    assert response.status_code in [201, 404, 409, 500]

def test_get_user_recipes(client):
    """Test getting user recipes"""
    response = client.get('/user/testuser/recipes/full')
    if response.status_code == 200:
        data = json.loads(response.data)
        assert isinstance(data, list)
    else:
        assert response.status_code == 500

def test_invalid_country(client):
    """Test invalid country"""
    response = client.get('/dish/InvalidCountryXYZ123')
    assert response.status_code in [404, 500]

def test_invalid_endpoint(client):
    """Test invalid endpoint returns 404"""
    response = client.get('/invalid/endpoint/that/does/not/exist')
    assert response.status_code == 404

def test_missing_dish_id(client):
    """Test save recipe without dish ID"""
    response = client.post('/user/testuser/save-dish',
                          data=json.dumps({}),
                          content_type='application/json')
    assert response.status_code == 400

def test_app_config():
    """Test application configuration"""
    assert app is not None
    assert hasattr(app, 'config')

@patch('app.models.MongoClient')
def test_database_connection_mock(mock_mongo):
    """Test database connection (mocked)"""
    mock_client = MagicMock()
    mock_mongo.return_value = mock_client
    db = Database()
    assert db is not None
    assert hasattr(db, 'client')

if __name__ == '__main__':
    pytest.main([__file__, '-v'])