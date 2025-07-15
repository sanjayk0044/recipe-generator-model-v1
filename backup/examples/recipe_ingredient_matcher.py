#!/usr/bin/env python3
"""
Recipe Ingredient Matcher

This script integrates the grocery catalog with the recipe generator API.
It allows the LLM model to query the catalog and suggest recipes based on available ingredients.
"""

import csv
import json
import os
import sys
import pandas as pd
from typing import List, Dict, Any, Optional

# Add the parent directory to the path so we can import from the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.services.gemini_service import GeminiService
except ImportError:
    print("Warning: Could not import GeminiService. Using mock service instead.")
    
    class GeminiService:
        """Mock Gemini service for testing."""
        
        def __init__(self, api_key=None):
            self.api_key = api_key or "mock_api_key"
            print("Initialized mock Gemini service")
            
        def generate_recipes(self, preferences):
            """Mock recipe generation."""
            print(f"Would generate recipes with preferences: {preferences}")
            return [{"title": "Mock Recipe", "ingredients": {"necessary_items": ["ingredient1", "ingredient2"]}}]


class RecipeIngredientMatcher:
    """Class to match recipe ingredients with grocery catalog items."""
    
    def __init__(self, catalog_file: str = "simple_grocery_catalog.csv"):
        """Initialize with the catalog file."""
        self.catalog_df = pd.read_csv(catalog_file)
        self.unique_items = self.catalog_df['item_name'].unique()
        self.categories = self.catalog_df['category'].unique()
        
        # Group by item_name to get all available packet sizes
        self.item_packets = {}
        for item_name in self.unique_items:
            packets = self.catalog_df[self.catalog_df['item_name'] == item_name]['packet_weight_grams'].tolist()
            self.item_packets[item_name] = packets
        
        # Initialize Gemini service
        try:
            self.gemini_service = GeminiService()
        except Exception as e:
            print(f"Error initializing Gemini service: {e}")
            self.gemini_service = None
    
    def get_available_ingredients(self, category: Optional[str] = None) -> List[str]:
        """Get a list of available ingredients, optionally filtered by category."""
        if category:
            return self.catalog_df[self.catalog_df['category'] == category]['item_name'].unique().tolist()
        return self.unique_items.tolist()
    
    def search_ingredients(self, query: str) -> List[Dict[str, Any]]:
        """Search for ingredients matching the query."""
        results = []
        query = query.lower()
        
        for item_name in self.unique_items:
            if query in item_name.lower():
                item_data = self.catalog_df[self.catalog_df['item_name'] == item_name].iloc[0]
                results.append({
                    'item_name': item_name,
                    'category': item_data['category'],
                    'packet_sizes': self.item_packets[item_name]
                })
        
        return results
    
    def generate_recipe_prompt(self, ingredients: List[str], preferences: Dict[str, Any]) -> str:
        """Generate a prompt for the LLM to create a recipe with the given ingredients."""
        ingredients_str = ", ".join(ingredients)
        
        prompt = f"""
        Create a recipe using the following ingredients from my grocery catalog:
        {ingredients_str}
        
        Additional preferences:
        """
        
        for key, value in preferences.items():
            prompt += f"- {key}: {value}\n"
        
        prompt += """
        Please provide:
        1. Recipe title
        2. Brief summary
        3. List of ingredients with quantities
        4. Step-by-step instructions
        5. Cooking time
        6. Difficulty level
        
        Only use ingredients from the provided list. If essential ingredients are missing, suggest alternatives from the list.
        """
        
        return prompt
    
    def suggest_recipes(self, ingredients: List[str], preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest recipes based on available ingredients."""
        if not self.gemini_service:
            print("Gemini service not available. Cannot generate recipes.")
            return []
        
        # Validate ingredients against catalog
        valid_ingredients = []
        for ingredient in ingredients:
            matches = self.search_ingredients(ingredient)
            if matches:
                valid_ingredients.append(matches[0]['item_name'])
        
        if not valid_ingredients:
            print("No valid ingredients found in the catalog.")
            return []
        
        # Generate recipes using the Gemini service
        try:
            # Combine ingredients and preferences for the API call
            api_preferences = preferences.copy()
            api_preferences['ingredients_to_include'] = valid_ingredients
            
            recipes = self.gemini_service.generate_recipes(api_preferences)
            return recipes
        except Exception as e:
            print(f"Error generating recipes: {e}")
            return []
    
    def check_recipe_ingredients(self, recipe: Dict[str, Any]) -> Dict[str, Any]:
        """Check if all ingredients in a recipe are available in the catalog."""
        if 'ingredients' not in recipe or 'necessary_items' not in recipe['ingredients']:
            return {'available': False, 'missing': [], 'available_ingredients': []}
        
        necessary_items = recipe['ingredients']['necessary_items']
        available = []
        missing = []
        
        for item in necessary_items:
            # Extract the base ingredient name (remove quantities and preparations)
            base_item = item.split(' ')[-1].lower()
            
            # Check if any catalog item contains this ingredient
            found = False
            for catalog_item in self.unique_items:
                if base_item in catalog_item.lower():
                    available.append(catalog_item)
                    found = True
                    break
            
            if not found:
                missing.append(item)
        
        return {
            'available': len(missing) == 0,
            'missing': missing,
            'available_ingredients': available
        }

def main():
    """Main function to demonstrate the recipe ingredient matcher."""
    catalog_file = "simple_grocery_catalog.csv"
    matcher = RecipeIngredientMatcher(catalog_file)
    
    print(f"Loaded grocery catalog with {len(matcher.unique_items)} unique items.")
    
    # Example: Search for ingredients
    search_term = "chicken"
    results = matcher.search_ingredients(search_term)
    print(f"\nSearch results for '{search_term}':")
    for result in results[:5]:  # Show first 5 results
        print(f"- {result['item_name']} ({result['category']}): {result['packet_sizes']}g packets")
    
    # Example: Get ingredients by category
    category = "Vegetables"
    vegetables = matcher.get_available_ingredients(category)
    print(f"\nSample {category} (first 5):")
    for veg in vegetables[:5]:
        print(f"- {veg}")
    
    # Example: Generate a recipe prompt
    ingredients = ["Chicken Breast", "Rice", "Bell Pepper", "Onion", "Garlic"]
    preferences = {
        "cuisine": "Asian",
        "cooking_time": "30min",
        "dietary": "none"
    }
    
    prompt = matcher.generate_recipe_prompt(ingredients, preferences)
    print("\nExample Recipe Prompt:")
    print(prompt)
    
    # Example: Check if we have ingredients for a sample recipe
    sample_recipe = {
        "title": "Simple Chicken Stir Fry",
        "ingredients": {
            "necessary_items": [
                "2 chicken breasts",
                "1 cup rice",
                "1 bell pepper",
                "1 onion",
                "2 cloves garlic",
                "3 tbsp soy sauce"
            ],
            "optional_items": [
                "1 tbsp sesame oil",
                "1 tsp ginger"
            ]
        }
    }
    
    check_result = matcher.check_recipe_ingredients(sample_recipe)
    print("\nRecipe Ingredient Check:")
    print(f"All ingredients available: {check_result['available']}")
    if not check_result['available']:
        print(f"Missing ingredients: {check_result['missing']}")
    print(f"Available ingredients: {check_result['available_ingredients']}")
    
    # Example: Suggest recipes (this would call the Gemini API in a real scenario)
    print("\nSuggesting recipes (mock):")
    suggested_recipes = matcher.suggest_recipes(ingredients, preferences)
    print(f"Generated {len(suggested_recipes)} recipes")

if __name__ == "__main__":
    main()
