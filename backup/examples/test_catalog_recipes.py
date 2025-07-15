#!/usr/bin/env python3
"""
Test Catalog-Integrated Recipe Generator

This script demonstrates how the grocery catalog integration works with the recipe generator API.
"""

import os
import sys
import json
from typing import Dict, Any

# Add the parent directory to the path so we can import from the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.services.gemini_service import generate_recipes
    from app.services.catalog_integration import get_integration_service
    
    # Check if we have a valid API key
    api_key_available = os.getenv("GEMINI_API_KEY") is not None
except ImportError:
    print("Warning: Could not import required modules. Make sure you're running this script from the correct directory.")
    api_key_available = False

def test_recipe_generation():
    """Test recipe generation with catalog integration."""
    if not api_key_available:
        print("No Gemini API key found. Skipping actual API calls.")
        return
    
    # Initialize catalog service
    catalog_service = get_integration_service()
    print(f"Loaded grocery catalog with {len(catalog_service.unique_items)} unique items.")
    
    # Test cases with different preferences
    test_cases = [
        {
            "name": "Simple Italian Pasta",
            "preferences": {
                "cuisine": "Italian",
                "meal_type": "dinner",
                "cooking_time": "30min",
                "ingredients_to_include": ["pasta", "tomato", "cheese"]
            }
        },
        {
            "name": "Asian Stir Fry",
            "preferences": {
                "cuisine": "Asian",
                "meal_type": "dinner",
                "cooking_time": "20min",
                "ingredients_to_include": ["rice", "chicken", "vegetables"]
            }
        },
        {
            "name": "Vegetarian Salad",
            "preferences": {
                "cuisine": "Mediterranean",
                "meal_type": "lunch",
                "dietary": "vegetarian",
                "cooking_time": "15min",
                "ingredients_to_include": ["lettuce", "cucumber", "olive oil"]
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n\n=== Testing: {test_case['name']} ===")
        
        # Search for ingredients in the catalog
        preferences = test_case["preferences"]
        for ingredient in preferences.get("ingredients_to_include", []):
            results = catalog_service.search_ingredients(ingredient)
            print(f"\nSearch results for '{ingredient}':")
            for result in results[:3]:  # Show first 3 results
                print(f"- {result['item_name']} ({result['category']}): {result['packet_sizes']}g packets")
        
        # Generate recipe
        print("\nGenerating recipe...")
        try:
            recipes = generate_recipes(preferences)
            
            print(f"\nGenerated {len(recipes)} recipe(s):")
            for recipe in recipes:
                print(f"\nTitle: {recipe['title']}")
                print(f"Summary: {recipe['summary'][:100]}...")
                
                print("\nIngredients:")
                for item in recipe['ingredients']['necessary_items']:
                    print(f"- {item}")
                
                print("\nProcedure (excerpt):")
                print(f"{recipe['procedure'][:150]}...")
        except Exception as e:
            print(f"Error generating recipe: {e}")

def main():
    """Main function to run the test."""
    print("Testing catalog-integrated recipe generator...")
    test_recipe_generation()

if __name__ == "__main__":
    main()
