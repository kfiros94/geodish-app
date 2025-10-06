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
    
    // Set up initial button listeners
    refreshButtonHandlers();
    
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

// Function to ensure buttons remain clickable after DOM changes
function refreshButtonHandlers() {
    console.log('🔄 Refreshing button handlers...');
    
    // Re-get button elements in case DOM changed
    saveDishBtn = document.getElementById('saveDish');
    getAnotherDishBtn = document.getElementById('getAnotherDish');
    
    // Remove old event listeners and add new ones
    if (saveDishBtn) {
        // Remove existing handlers
        saveDishBtn.replaceWith(saveDishBtn.cloneNode(true));
        saveDishBtn = document.getElementById('saveDish');
        
        saveDishBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('💾 Save button clicked');
            saveCurrentDish();
        });
    }
    
    if (getAnotherDishBtn) {
        // Remove existing handlers
        getAnotherDishBtn.replaceWith(getAnotherDishBtn.cloneNode(true));
        getAnotherDishBtn = document.getElementById('getAnotherDish');
        
        getAnotherDishBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('🎲 Get another dish button clicked');
            if (selectedCountry) {
                getRandomDishForCountry(selectedCountry);
            } else {
                showAlert('Please select a country first', 'warning');
            }
        });
    }
    
    console.log('✅ Button handlers refreshed');
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
        
        // ✅ FIXED: Handle direct array format from API
        if (Array.isArray(data)) {
            // Direct array format: ["Argentina", "Australia"...]
            displayCountriesGrid(data);
        } else if (data && data.countries && Array.isArray(data.countries)) {
            // Nested format: {countries: ["Argentina"...]}
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
    
    // Complete emoji flags for all 24 countries
    const countryEmojis = {
        'Italy': '🇮🇹',
        'France': '🇫🇷',
        'Japan': '🇯🇵',
        'India': '🇮🇳',
        'Mexico': '🇲🇽',
        'China': '🇨🇳',
        'Thailand': '🇹🇭',
        'Spain': '🇪🇸',
        'Greece': '🇬🇷',
        'Turkey': '🇹🇷',
        'Morocco': '🇲🇦',
        'Brazil': '🇧🇷',
        'Argentina': '🇦🇷',
        'Peru': '🇵🇪',
        'South Korea': '🇰🇷',
        'Lebanon': '🇱🇧',
        'Russia': '🇷🇺',
        'Ethiopia': '🇪🇹',
        'Nigeria': '🇳🇬',
        'USA': '🇺🇸',
        'United Kingdom': '🇬🇧',
        'Germany': '🇩🇪',
        'Canada': '🇨🇦',
        'Australia': '🇦🇺'
    };
    
    const countriesHTML = countries.map(country => `
        <div class="col-xl-2 col-lg-2 col-md-3 col-sm-4 col-6 mb-4">
            <div class="country-card text-center" onclick="selectCountry('${country}')">
                <div class="card-body">
                    <img src="/static/images/flags/${country.toLowerCase()}.png" 
                         alt="${country} flag" 
                         class="country-flag"
                         style="display: block;"
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='block';"
                         onload="console.log('✅ Loaded PNG flag for ${country}');">
                    
                    <div class="country-flag-emoji" style="display: none;">
                        ${countryEmojis[country] || '🏴'}
                    </div>
                    
                    <h6 class="card-title">${country}</h6>
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
                <div class="alert alert-warning">
                    <h5>🌍 Unable to load countries</h5>
                    <p>Please try refreshing the page or contact support.</p>
                    <button class="btn btn-primary" onclick="loadCountries()">Try Again</button>
                </div>
            </div>
        `;
    }
}

// Country selection
function selectCountry(country) {
    console.log('🌍 Selected country:', country);
    selectedCountry = country;
    
    // Clear previous selection
    document.querySelectorAll('.country-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Mark selected country
    event.currentTarget.classList.add('selected');
    
    // Get random dish from selected country
    getRandomDishForCountry(country);
}

// Get random dish for country
async function getRandomDishForCountry(country) {
    console.log(`🎲 Getting random dish from ${country}...`);
    
    try {
        // ✅ FIXED: Match the correct API endpoint
        const response = await fetch(`/dish/${country}`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const dish = await response.json();
        console.log('🍽️ Random dish received:', dish);
        displayDish(dish);
        
    } catch (error) {
        console.error('❌ Error getting random dish:', error);
        showAlert(`Failed to load dish from ${country}: ${error.message}`, 'danger');
    }
}

// Display dish with image support
function displayDish(dish) {
    console.log('🍽️ Displaying dish:', dish);
    
    if (!dish) {
        console.error('❌ No dish data provided');
        return;
    }
    
    // Hide "no dish selected" message
    noDishSelected.style.display = 'none';
    dishDisplay.style.display = 'block';
    
    // Store current dish
    currentDish = dish;
    
    // Create dish image filename from dish name
    const imageFilename = dish.name.toLowerCase()
        .replace(/\s+/g, '-')
        .replace(/[^a-z0-9-]/g, '');
    
    // Country emoji mapping
    const countryEmojis = {
        'Italy': '🇮🇹',
        'France': '🇫🇷',
        'Japan': '🇯🇵',
        'India': '🇮🇳',
        'Mexico': '🇲🇽',
        'China': '🇨🇳',
        'Thailand': '🇹🇭',
        'Spain': '🇪🇸',
        'Greece': '🇬🇷',
        'Turkey': '🇹🇷',
        'Morocco': '🇲🇦',
        'Brazil': '🇧🇷',
        'Argentina': '🇦🇷',
        'Peru': '🇵🇪',
        'South Korea': '🇰🇷',
        'Lebanon': '🇱🇧',
        'Russia': '🇷🇺',
        'Ethiopia': '🇪🇹',
        'Nigeria': '🇳🇬',
        'USA': '🇺🇸',
        'United Kingdom': '🇬🇧',
        'Germany': '🇩🇪',
        'Canada': '🇨🇦',
        'Australia': '🇦🇺'
    };
    
    // Update dish information FIRST
    dishName.textContent = dish.name;
    const countryEmoji = countryEmojis[dish.country] || '🏴';
    dishCountry.textContent = `From ${dish.country} ${countryEmoji}`;
    
    // Update ingredients
    dishIngredients.innerHTML = dish.ingredients.map(ingredient => 
        `<li class="list-group-item">${ingredient}</li>`
    ).join('');
    
    // Update instructions
    dishInstructions.textContent = dish.instructions;
    
    // Remove any existing dish image
    const existingImage = dishDisplay.querySelector('.dish-image-container');
    if (existingImage) {
        existingImage.remove();
    }
    
    // Create and insert dish image AFTER updating content
    const dishImageContainer = document.createElement('div');
    dishImageContainer.className = 'dish-image-container mb-3 text-center';
    dishImageContainer.innerHTML = `
        <img src="/static/images/dishes/${imageFilename}.png" 
             alt="${dish.name}" 
             class="dish-image img-fluid"
             onerror="this.onerror=null; this.src='/static/images/dishes/${imageFilename}.jpg'; console.log('⚠️ PNG not found, trying JPG for ${dish.name}');"
             onload="console.log('✅ Loaded image for ${dish.name}');">
    `;
    
    // Insert image after the country badge but before ingredients
    const countryElement = dishCountry.parentElement;
    if (countryElement && countryElement.nextElementSibling) {
        countryElement.parentElement.insertBefore(dishImageContainer, countryElement.nextElementSibling);
    } else {
        // Fallback: insert at the beginning of dishDisplay
        dishDisplay.insertBefore(dishImageContainer, dishDisplay.firstChild.nextSibling);
    }
    
    // IMPORTANT: Refresh button handlers after DOM changes
    setTimeout(() => {
        refreshButtonHandlers();
    }, 100);
    
    console.log(`✅ Successfully displayed dish: ${dish.name} from ${dish.country}`);
}

// Save current dish to user's recipes
async function saveCurrentDish() {
    console.log('💾 Saving current dish:', currentDish);
    
    if (!currentDish) {
        showAlert('No dish selected to save', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`/user/${currentUserId}/save-dish`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                dish_id: currentDish._id,
                custom_name: currentDish.name
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json();
        console.log('✅ Dish saved successfully:', result);
        
        showAlert(`${currentDish.name} saved to your recipes!`, 'success');
        
        // Reload user recipes to show the new addition
        loadUserRecipes();
        
    } catch (error) {
        console.error('❌ Error saving dish:', error);
        showAlert('Failed to save recipe: ' + error.message, 'danger');
    }
}

// Load and display user's saved recipes
async function loadUserRecipes() {
    console.log('📚 Loading user recipes...');
    
    try {
        const response = await fetch(`/user/${currentUserId}/recipes/full`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('📊 User recipes received:', data);
        
        // ✅ FIXED: Handle direct array format from API
        if (Array.isArray(data)) {
            displayUserRecipes(data);
        } else if (data && data.recipes && Array.isArray(data.recipes)) {
            displayUserRecipes(data.recipes);
        } else {
            displayUserRecipes([]);
        }
        
    } catch (error) {
        console.error('❌ Error loading user recipes:', error);
        displayUserRecipes([]);
    }
}

function displayUserRecipes(recipes) {
    console.log('🍴 Displaying user recipes:', recipes);
    
    if (!savedRecipesDiv) {
        console.error('❌ Saved recipes div not found');
        return;
    }
    
    if (recipes.length === 0) {
        savedRecipesDiv.innerHTML = `
            <div class="text-center py-5">
                <h5>📖 No saved recipes yet</h5>
                <p class="text-muted">Start discovering dishes to build your personal cookbook!</p>
                <a href="#countries-section" class="btn btn-primary">Start Exploring</a>
            </div>
        `;
        return;
    }
    
    const recipesHTML = recipes.map(recipe => `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card recipe-card h-100">
                <div class="card-body">
                    <h6 class="card-title">${recipe.custom_name || recipe.dish_name || 'Unknown Recipe'}</h6>
                    <p class="card-text">
                        <small class="text-muted">From ${recipe.country || 'Unknown'}</small>
                    </p>
                    <p class="card-text">${recipe.ingredients?.join(', ') || 'No ingredients listed'}</p>
                    <p class="card-text"><small>${recipe.instructions || 'No instructions available'}</small></p>
                </div>
                <div class="card-footer">
                    <button class="btn btn-sm btn-danger" onclick="deleteRecipe('${recipe._id}')">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
            </div>
        </div>
    `).join('');
    
    savedRecipesDiv.innerHTML = recipesHTML;
    console.log(`✅ Successfully displayed ${recipes.length} recipes`);
}

// Delete a saved recipe
async function deleteRecipe(recipeId) {
    console.log('🗑️ Deleting recipe:', recipeId);
    
    if (!confirm('Are you sure you want to delete this recipe?')) {
        return;
    }
    
    try {
        const response = await fetch(`/user/${currentUserId}/recipes/${recipeId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json();
        console.log('✅ Recipe deleted successfully:', result);
        
        showAlert('Recipe deleted successfully!', 'success');
        
        // Reload user recipes to remove the deleted item
        loadUserRecipes();
        
    } catch (error) {
        console.error('❌ Error deleting recipe:', error);
        showAlert('Failed to delete recipe: ' + error.message, 'danger');
    }
}

// Search functionality
async function searchDish() {
    const searchTerm = searchInput?.value?.trim();
    
    if (!searchTerm) {
        showAlert('Please enter a search term', 'warning');
        return;
    }
    
    console.log('🔍 Searching for:', searchTerm);
    showAlert('Search functionality coming soon!', 'info');
}

// Utility function to show alerts
function showAlert(message, type) {
    // Remove existing alerts
    document.querySelectorAll('.alert-custom').forEach(alert => alert.remove());
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show alert-custom`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv && alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
    
    console.log(`📢 Alert (${type}): ${message}`);
}
