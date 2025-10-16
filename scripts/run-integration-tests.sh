#!/bin/bash
set -e  # Exit on error

echo "================================"
echo "🧪 Running Integration Tests"
echo "================================"

# Wait for MongoDB to be ready
echo "⏳ Waiting for MongoDB..."
until mongosh --eval "db.adminCommand('ping')" mongodb:27017/geodish_test --quiet; do
  echo "MongoDB not ready, waiting..."
  sleep 2
done
echo "✅ MongoDB is ready!"

# Install test dependencies
echo "📦 Installing test dependencies..."
pip install -q pytest

# Seed the database
echo "🌱 Seeding test database..."
python3 -c "
from app.models import Database
from app.seed_manager import SeedManager
db = Database()
sm = SeedManager(db)
result = sm.seed_database(force=True)
print(f'✅ {result}')
"

# Run integration tests
echo "🧪 Running integration tests..."
python3 -m pytest tests/test.py -v --tb=short

# Check results
if [ $? -eq 0 ]; then
    echo "================================"
    echo "✅ All integration tests passed!"
    echo "================================"
    exit 0
else
    echo "================================"
    echo "❌ Integration tests failed!"
    echo "================================"
    exit 1
fi