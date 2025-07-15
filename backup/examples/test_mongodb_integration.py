#!/usr/bin/env python3
"""
Test MongoDB Catalog Integration

This script tests the MongoDB catalog integration with the recipe generator API.
"""

import os
import sys
import json
from typing import Dict, Any

# Add the parent directory to the path so we can import from the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.services.mongodb_service import get_mongodb_service
    from app.services.catalog_integration import get_integration_service
    from app.services.gemini_service import generate_recipes
    
    # Check if we have a valid API key
    api_key_available = os.getenv("GEMINI_API_KEY") is not None
except ImportError as e:
    print(f"Warning: Could not import required modules: {e}")
    print("Make sure you're running this script from the correct directory.")
    api_key_available = False

def test_mongodb_service():
    """Test the MongoDB service."""
    print("\n=== Testing MongoDB Service ===")
    
    try:
        # Initialize MongoDB service
        mongodb_service = get_mongodb_service()
        
        # Get all categories
        categories = mongodb_service.get_all_categories()
        print(f"Available categories: {', '.join(categories)}")
        
        # Get random ingredients
        random_ingredients = mongodb_service.get_random_ingredients(5)
        print("\nRandom ingredients:")
        for ingredient in random_ingredients:
            print(f"- {ingredient['item_name']} ({ingredient['category']})")
            for packet in ingredient['packet_sizes']:
                print(f"  * {packet['weight']}g: ${packet['price']}")
        
        # Search for ingredients
        search_term = "chicken"
        search_results = mongodb_service.search_items(search_term)
        print(f"\nSearch results for '{search_term}':")
        for i, result in enumerate(search_results[:5]):
            print(f"- {result['item_name']} ({result['category']}): {result['packet_weight_grams']}g, ${result['price']}")
            if i >= 4:
                print(f"... and {len(search_results) - 5} more results")
                break
        
        return True
    except Exception as e:
        print(f"Error testing MongoDB service: {e}")
        return False

def test_catalog_integration():
    """Test the catalog integration service."""
    print("\n=== Testing Catalog Integration Service ===")
    
    try:
        # Initialize catalog integration service
        integration_service = get_integration_service()
        
        # Get available ingredients by category
        category = "Vegetables"
        vegetables = integration_service.get_available_ingredients(category)
        print(f"\nSample {category} (first 5):")
        for veg in vegetables[:5]:
            print(f"- {veg['item_name']}")
        
        # Test prompt enhancement
        preferences = {
            "cuisine": "Italian",
            "meal_type": "dinner",
            "cooking_time": "30min",
            "ingredients_to_include": ["pasta", "tomato", "cheese"]
        }
        
        base_prompt = "Generate a recipe based on the following preferences."
        enhanced_prompt = integration_service.enhance_recipe_prompt(base_prompt, preferences)
        
        print("\nEnhanced prompt excerpt:")
        print("\n".join(enhanced_prompt.split("\n")[:10]) + "\n...")
        
        return True
    except Exception as e:
        print(f"Error testing catalog integration: {e}")
        return False

def test_recipe_generation():
    """Test recipe generation with MongoDB catalog integration."""
    print("\n=== Testing Recipe Generation with Catalog Integration ===")
    
    if not api_key_available:
        print("No Gemini API key found. Skipping recipe generation test.")
        return False
    
    try:
        # Generate a recipe with catalog integration
        preferences = {
            "cuisine": "Italian",
            "meal_type": "dinner",
            "cooking_time": "30min",
            "ingredients_to_include": ["pasta", "tomato", "cheese"]
        }
        
        print("Generating recipe...")
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
        
        return True
    except Exception as e:
        print(f"Error testing recipe generation: {e}")
        return False

def main():
    """Main function to run the tests."""
    print("Testing MongoDB catalog integration...")
    
    # Install required packages if needed
    try:
        import pymongo
    except ImportError:
        print("Installing required packages...")
        os.system("pip install pymongo")
    
    # Run tests
    mongodb_test = test_mongodb_service()
    if mongodb_test:
        integration_test = test_catalog_integration()
        if integration_test and api_key_available:
            recipe_test = test_recipe_generation()
    
    print("\nTests completed!")

if __name__ == "__main__":
    main()
