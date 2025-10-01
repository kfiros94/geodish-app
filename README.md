# 🌍 GeoDish - World Cuisine Discovery App

A Flask-based REST API application that helps users discover traditional dishes from around the world. Users can explore cuisines from 20 different countries and save their favorite recipes.

## 🚀 Features

- **Country-based Discovery**: Choose from 20 countries to explore their traditional dishes
- **Random Dish Selection**: Get random dish recommendations from your selected country
- **Recipe Saving**: Save interesting dishes to your personal recipe collection
- **REST API**: Complete API for integration with other applications
- **Responsive UI**: Simple web interface for easy interaction
- **Docker Support**: Fully containerized application with MongoDB

## 🏗️ Architecture

- **Backend**: Python Flask with REST API
- **Database**: MongoDB for storing dishes and user recipes
- **Frontend**: Static HTML/CSS/JavaScript served by Nginx
- **Containerization**: Docker with multi-stage builds
- **Reverse Proxy**: Nginx for serving static files and proxying API calls

## 📋 API Endpoints

### Dishes
- `GET /countries` - List all available countries
- `GET /dish/random/{country}` - Get random dish from specified country
- `GET /dish/{dish_id}` - Get specific dish by ID
- `GET /dishes/{country}` - Get all dishes from a country

### User Recipes
- `POST /user/{user_id}/recipes` - Save dish to user's recipes
- `GET /user/{user_id}/recipes` - Get user's saved recipes
- `DELETE /user/{user_id}/recipes/{recipe_id}` - Delete saved recipe

### Utility
- `GET /metrics` - Health check and app metrics
- `POST /seed` - Seed database with sample dishes
- `GET /` - Serve main web interface

## 🛠️ Technology Stack

- **Backend**: Python 3.11, Flask 2.3.3
- **Database**: MongoDB 7.0
- **Web Server**: Nginx (Alpine)
- **Containerization**: Docker, Docker Compose
- **Testing**: Pytest
- **Frontend**: Vanilla HTML/CSS/JavaScript

## 🚦 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Installation & Running

1. **Clone the repository**
