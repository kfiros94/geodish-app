// GeoDish Enhanced App JavaScript
const API_BASE = '';
let currentUserId = 'user123';
let currentDish = null;
let selectedCountry = null;

// DOM Elements
let countriesGrid;
let dishDisplay;
let noDishSelected;
let dishName;
let dishCountry;
let dishIngredients;
let dishInstructions;
let saveDishBtn;
let getAnotherDishBtn;
let savedRecipesDiv;
let searchInput;
let searchBtn;
let themeToggle;

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    console.log('🌍 GeoDish Enhanced App Starting...');
    
    // Get DOM elements
    initializeDOMElements();
    
    // Setup event listeners
    setupEventListeners();
    
    // Initialize components
    loadCountries();
    loadUserRecipes();
    
    // Initialize theme
    initializeTheme();
    
    console.log('✅ GeoDish Enhanced App Initialized');
});

function initializeDOMElements() {
    countriesGrid = document.getElementById('countriesGrid');
    dishDisplay = document.getElementById('dishDisplay');
    noDishSelected = document.getElementById('noDishSelected');
    dishName = document.getElementById('dishName');
    dishCountry = document.getElementById('dishCountry');
    dishIngredients = document.getElementById('dishIngredients');
    dishInstructions = document.getElementById('dishInstructions');
    saveDishBtn = document.getElementById('saveDish');
    getAnotherDishBtn = document.getElementById('getAnotherDish');
    savedRecipesDiv = document.getElementById('savedRecipes');
    searchInput = document.getElementById('searchInput');
    searchBtn = document.getElementById('searchBtn');
    themeToggle = document.getElementById('themeToggle');
}

function setupEventListeners() {
    // Theme toggle
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
    
    // Search functionality
    if (searchBtn) {
        searchBtn.addEventListener('click', searchDish);
    }
    
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchDish();
            }
        });
    }
    
    // Dish actions
    if (saveDishBtn) {
        saveDishBtn.addEventListener('click', saveDish);
    }
    
    if (getAnotherDishBtn) {
        getAnotherDishBtn.addEventListener('click', getAnotherDish);
    }
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Theme Management
function initializeTheme() {
    const savedTheme = localStorage.getItem('geodish-theme') || 'light';
    setTheme(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-bs-theme', theme);
    localStorage.setItem('geodish-theme', theme);
    
    const themeIcon = document.getElementById('themeIcon');
    if (themeIcon) {
        themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
}

// Load and display countries in grid format
async function loadCountries() {
    console.log('📡 Loading countries...');
    
    try {
        const response = await fetch('/countries');
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('📊 Countries data received:', data);
        
        if (data && data.countries && Array.isArray(data.countries)) {
            displayCountriesGrid(data.countries);
        } else {
            throw new Error('Invalid countries data format');
        }
        
    } catch (error) {
        console.error('❌ Error loading countries:', error);
        showAlert('Failed to load countries: ' + error.message, 'danger');
        displayCountriesError();
    }
}

function displayCountriesGrid(countries) {
    console.log('🌍 Displaying countries grid:', countries);
    
    if (!countriesGrid) {
        console.error('❌ Countries grid element not found');
        return;
    }
    
    // Country flag URLs (you can replace these with actual flag images)
    const countryFlags = {
        'Italy': '🇮🇹',
        'France': '🇫🇷',
        'Japan': '🇯🇵',
        'India': '🇮🇳',
        'Mexico': '🇲🇽'
    };
    
    const countriesHTML = countries.map(country => `
        <div class="col-lg-2 col-md-3 col-sm-4 col-6">
            <div class="card country-card h-100 text-center p-3" onclick="selectCountry('${country}')">
                <div class="card-body">
                    <div class="country-flag-emoji mb-3" style="font-size: 3rem;">
                        ${countryFlags[country] || '🏴'}
                    </div>
                    <h6 class="card-title mb-0">${country}</h6>
                </div>
            </div>
        </div>
    `).join('');
    
    countriesGrid.innerHTML = countriesHTML;
    console.log(`✅ Successfully displayed ${countries.length} countries`);
}

function displayCountriesError() {
    if (countriesGrid) {
        countriesGrid.innerHTML = `
            <div class="col-12 text-center">
                <div class="alert alert-danger" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Failed to load countries. Please try refreshing the page.
                </div>
            </div>
        `;
    }
}

// Country selection
function selectCountry(country) {
    console.log('🌍 Country selected:', country);
    selectedCountry = country;
    
    // Update visual selection
    document.querySelectorAll('.country-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    event.target.closest('.country-card').classList.add('selected');
    
    // Get random dish from selected country
    getRandomDish(country);
    
    // Scroll to dish section
    document.getElementById('dish-section').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Get random dish from selected country
async function getRandomDish(country = selectedCountry) {
    if (!country) {
        showAlert('Please select a country first', 'warning');
        return;
    }
    
    console.log('🎲 Getting random dish for:', country);
    
    try {
        showDishLoading(true);
        
        const response = await fetch(`/dish/random/${encodeURIComponent(country)}`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('🍽️ Dish data received:', data);
        
        currentDish = data;
        displayDish(data);
        
    } catch (error) {
        console.error('❌ Error getting random dish:', error);
        showAlert('Failed to get dish: ' + error.message, 'danger');
        showDishLoading(false);
    }
}

// Get another dish from the same country
function getAnotherDish() {
    if (selectedCountry) {
        getRandomDish(selectedCountry);
    }
}

function showDishLoading(loading) {
    if (loading) {
        dishDisplay.style.display = 'block';
        noDishSelected.style.display = 'none';
        
        if (dishName) dishName.innerHTML = '<div class="loading-spinner me-2"></div>Loading...';
        if (dishCountry) dishCountry.textContent = 'Loading...';
        if (dishIngredients) dishIngredients.textContent = 'Loading ingredients...';
        if (dishInstructions) dishInstructions.textContent = 'Loading instructions...';
        
        if (saveDishBtn) saveDishBtn.disabled = true;
        if (getAnotherDishBtn) getAnotherDishBtn.disabled = true;
    } else {
        dishDisplay.style.display = 'none';
        noDishSelected.style.display = 'block';
    }
}

// Display dish information
function displayDish(dish) {
    console.log('🖼️ Displaying dish:', dish.name);
    
    if (dishName) dishName.textContent = dish.name || 'Unknown Dish';
    if (dishCountry) dishCountry.textContent = dish.country || 'Unknown';
    if (dishIngredients) dishIngredients.textContent = dish.ingredients?.join(', ') || 'No ingredients listed';
    if (dishInstructions) dishInstructions.textContent = dish.instructions || 'No instructions available';
    
    if (dishDisplay) {
        dishDisplay.style.display = 'block';
        noDishSelected.style.display = 'none';
    }
    
    if (saveDishBtn) saveDishBtn.disabled = false;
    if (getAnotherDishBtn) getAnotherDishBtn.disabled = false;
}

// Search functionality
async function searchDish() {
    const query = searchInput?.value?.trim();
    if (!query) {
        showAlert('Please enter a dish name to search', 'warning');
        return;
    }
    
    console.log('🔍 Searching for dish:', query);
    showAlert('Search functionality coming soon!', 'info');
    
    // TODO: Implement dish search functionality
    // This would require a new API endpoint for searching dishes
}

// Save dish to user recipes
async function saveDish() {
    console.log('💾 Saving dish to recipes...');
    
    if (!currentDish) {
        showAlert('No dish selected to save', 'warning');
        return;
    }

    try {
        saveDishBtn.disabled = true;
        saveDishBtn.innerHTML = '<div class="loading-spinner me-2"></div>Saving...';
        
        const response = await fetch(`/user/${currentUserId}/recipes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                dish_id: currentDish._id
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert(`"${currentDish.name}" saved to your recipes!`, 'success');
            loadUserRecipes(); // Refresh the recipes list
        } else {
            if (response.status === 400 && data.error?.includes('already saved')) {
                showAlert('This dish is already in your recipes!', 'warning');
            } else {
                showAlert('Failed to save recipe: ' + (data.error || 'Unknown error'), 'danger');
            }
        }
    } catch (error) {
        console.error('❌ Error saving recipe:', error);
        showAlert('Error saving recipe: ' + error.message, 'danger');
    } finally {
        saveDishBtn.disabled = false;
        saveDishBtn.innerHTML = '<i class="fas fa-bookmark me-2"></i>Save to My Recipes';
    }
}

// Load user's saved recipes
async function loadUserRecipes() {
    console.log('📚 Loading user recipes...');
    
    try {
        const response = await fetch(`/user/${currentUserId}/recipes/full`);
        
        if (response.ok) {
            const data = await response.json();
            console.log('📚 Recipes loaded:', data);
            displayUserRecipes(data.recipes || []);
        } else {
            console.log('📚 No recipes found');
            displayUserRecipes([]);
        }
    } catch (error) {
        console.error('❌ Error loading recipes:', error);
        displayUserRecipes([]);
    }
}

// Display user's saved recipes
function displayUserRecipes(recipes) {
    console.log(`📚 Displaying ${recipes.length} recipes`);
    
    if (!savedRecipesDiv) {
        console.error('❌ Saved recipes div not found');
        return;
    }
    
    if (!recipes || recipes.length === 0) {
        savedRecipesDiv.innerHTML = `
            <div class="col-12 text-center">
                <i class="fas fa-clipboard-list display-1 text-muted mb-4"></i>
                <h4 class="text-muted">No saved recipes yet</h4>
                <p class="text-muted">Start discovering dishes to build your personal cookbook!</p>
                <a href="#countries" class="btn btn-primary">
                    <i class="fas fa-compass me-2"></i>Start Exploring
                </a>
            </div>
        `;
        return;
    }
    
    const recipesHTML = recipes.map(recipe => `
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="card recipe-card h-100">
                <div class="card-body">
                    <button class="recipe-delete-btn" onclick="deleteRecipe('${recipe._id}')" title="Remove recipe">
                        <i class="fas fa-times"></i>
                    </button>
                    
                    <h5 class="card-title">${recipe.custom_name || recipe.dish_name || 'Untitled Recipe'}</h5>
                    <span class="badge bg-primary mb-3">${recipe.country || 'Unknown'}</span>
                    
                    <div class="mb-3">
                        <h6 class="text-success"><i class="fas fa-list-ul me-1"></i> Ingredients:</h6>
                        <p class="small text-muted">${recipe.ingredients?.join(', ') || 'No ingredients listed'}</p>
                    </div>
                    
                    <div>
                        <h6 class="text-info"><i class="fas fa-book-open me-1"></i> Instructions:</h6>
                        <p class="small text-muted">${recipe.instructions || 'No instructions available'}</p>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
    
    savedRecipesDiv.innerHTML = recipesHTML;
}

// Delete a saved recipe
async function deleteRecipe(recipeId) {
    console.log('🗑️ Deleting recipe:', recipeId);
    
    if (!confirm('Are you sure you want to remove this recipe from your collection?')) {
        return;
    }

    try {
        const response = await fetch(`/user/${currentUserId}/recipes/${recipeId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('Recipe removed from your collection', 'success');
            loadUserRecipes(); // Refresh the list
        } else {
            showAlert('Failed to delete recipe: ' + (data.error || 'Unknown error'), 'danger');
        }
    } catch (error) {
        console.error('❌ Error deleting recipe:', error);
        showAlert('Error deleting recipe: ' + error.message, 'danger');
    }
}

// Show alert messages
function showAlert(message, type = 'info') {
    console.log(`📢 Showing ${type} alert:`, message);
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-custom alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Make functions globally available
window.selectCountry = selectCountry;
window.deleteRecipe = deleteRecipe;

console.log('📜 GeoDish Enhanced script loaded successfully');
