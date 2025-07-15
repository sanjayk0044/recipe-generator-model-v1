"""
Catalog Integration Service

This module integrates the grocery catalog with the recipe generator API.
It enhances the Gemini prompts with catalog information to ensure recipes
use ingredients available in the catalog.
"""

import os
import json
from typing import List, Dict, Any, Optional
from app.services.mongodb_service import get_mongodb_service

class CatalogIntegrationService:
    """Service to integrate grocery catalog with recipe generation."""
    
    def __init__(self):
        """Initialize with MongoDB service."""
        try:
            self.mongodb_service = get_mongodb_service()
            self.categories = self.mongodb_service.get_all_categories()
            print(f"Catalog integration initialized with {len(self.categories)} categories")
        except Exception as e:
            raise Exception(f"Failed to initialize catalog integration: {e}")
    
    def get_available_ingredients(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get a list of available ingredients, optionally filtered by category."""
        return self.mongodb_service.get_available_ingredients(category)
    
    def search_ingredients(self, query: str) -> List[Dict[str, Any]]:
        """Search for ingredients matching the query."""
        return self.mongodb_service.search_items(query)
    
    def enhance_recipe_prompt(self, prompt: str, preferences: Dict[str, Any]) -> str:
        """Enhance the recipe prompt with catalog information."""
        # Get ingredients from the catalog
        all_ingredients = []
        
        # If cuisine is specified, get ingredients commonly used in that cuisine
        if 'cuisine' in preferences:
            cuisine = preferences['cuisine'].lower()
            if cuisine == 'italian':
                categories = ['Vegetables', 'Dairy', 'Grains', 'Herbs']
            elif cuisine == 'asian':
                categories = ['Vegetables', 'Seafood', 'Grains', 'Spices']
            elif cuisine == 'mexican':
                categories = ['Vegetables', 'Meat', 'Grains', 'Spices']
            elif cuisine == 'indian':
                categories = ['Vegetables', 'Dairy', 'Grains', 'Spices']
            else:
                categories = ['Vegetables', 'Meat', 'Grains', 'Dairy']
                
            for category in categories:
                if category in self.categories:
                    category_ingredients = self.mongodb_service.get_items_by_category(category)
                    all_ingredients.extend(category_ingredients[:20])  # Limit to 20 items per category
        
        # If specific ingredients are requested, prioritize those
        if 'ingredients_to_include' in preferences and preferences['ingredients_to_include']:
            for ingredient in preferences['ingredients_to_include']:
                matches = self.search_ingredients(ingredient)
                if matches:
                    all_ingredients = matches + all_ingredients
        
        # If we don't have enough ingredients, get some random ones
        if len(all_ingredients) < 50:
            random_ingredients = self.mongodb_service.get_random_ingredients(50 - len(all_ingredients))
            all_ingredients.extend(random_ingredients)
        
        # Remove duplicates while preserving order (based on _id)
        seen_ids = set()
        unique_ingredients = []
        for ingredient in all_ingredients:
            if ingredient['_id'] not in seen_ids:
                seen_ids.add(ingredient['_id'])
                unique_ingredients.append(ingredient)
        
        # Limit to a reasonable number of ingredients (max 100)
        unique_ingredients = unique_ingredients[:100]
        
        # Create a structured list of ingredients for the LLM
        ingredient_list = []
        for ingredient in unique_ingredients:
            ingredient_list.append({
                "_id": ingredient['_id'],
                "item_name": ingredient['item_name'],
                "category": ingredient['category'],
                "packet_weight_grams": ingredient['packet_weight_grams'],
                "price": ingredient['price']
            })
        
        # Enhance the prompt with catalog information
        enhanced_prompt = prompt + "\n\n"
        enhanced_prompt += "IMPORTANT: You must ONLY use ingredients from the following catalog in your recipe. DO NOT invent or use any ingredients not listed here.\n\n"
        enhanced_prompt += "Available ingredients from the grocery catalog:\n"
        enhanced_prompt += json.dumps(ingredient_list, indent=2)
        
        enhanced_prompt += "\n\nIMPORTANT INSTRUCTIONS:"
        enhanced_prompt += "\n1. The necessary_items and optional_items in your response must ONLY contain _id values from this list."
        enhanced_prompt += "\n2. DO NOT make up or generate any _id values."
        enhanced_prompt += "\n3. Only use the exact _id strings provided in the catalog above."
        enhanced_prompt += "\n4. Make sure all ingredients needed for the recipe are available in the catalog."
        enhanced_prompt += "\n5. If you can't make a good recipe with these ingredients, say so rather than making up ingredients."
        
        return enhanced_prompt
    
    def validate_recipe_ingredients(self, recipes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and enhance recipe ingredients with catalog information."""
        validated_recipes = []
        
        for recipe in recipes:
            if 'ingredients' not in recipe:
                continue
                
            # Check if necessary_items contains MongoDB _ids
            if 'necessary_items' in recipe['ingredients']:
                necessary_ids = recipe['ingredients']['necessary_items']
                
                # Get the full ingredient details for display
                necessary_items_details = self.mongodb_service.get_items_by_mongodb_ids(necessary_ids)
                recipe['ingredients']['necessary_items_details'] = necessary_items_details
            
            # Do the same for optional_items
            if 'optional_items' in recipe['ingredients']:
                optional_ids = recipe['ingredients']['optional_items']
                
                # Get the full ingredient details for display
                optional_items_details = self.mongodb_service.get_items_by_mongodb_ids(optional_ids)
                recipe['ingredients']['optional_items_details'] = optional_items_details
            
            validated_recipes.append(recipe)
        
        return validated_recipes

def get_integration_service() -> CatalogIntegrationService:
    """Factory function to get a catalog integration service instance."""
    return CatalogIntegrationService()
