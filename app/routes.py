from flask import Blueprint, request, jsonify
from app.services.gemini_service import generate_recipes
from app.services.mongodb_service import get_mongodb_service
import json

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/health', methods=['GET'])
def get_recipes():
    return "OK"


def verify_recipe_ingredients(recipes):
    """
    Verify that all recipes have valid ingredients from the catalog
    
    Args:
        recipes (list): List of recipe dictionaries
        
    Returns:
        list: List of verified recipes
    """
    mongodb_service = get_mongodb_service()
    verified_recipes = []
    
    for recipe in recipes:
        if 'ingredients' not in recipe:
            continue
        
        # Verify necessary_items
        if 'necessary_items' in recipe['ingredients']:
            # Verify that all necessary_items exist in the database
            valid_ids = mongodb_service.verify_mongodb_ids(recipe['ingredients']['necessary_items'])
            
            # If we have valid necessary items, include this recipe
            if valid_ids:
                recipe['ingredients']['necessary_items'] = valid_ids
                
                # Get the full ingredient details
                necessary_items_details = mongodb_service.get_items_by_mongodb_ids(valid_ids)
                recipe['ingredients']['necessary_items_details'] = necessary_items_details
                
                # Verify optional_items
                if 'optional_items' in recipe['ingredients']:
                    valid_optional_ids = mongodb_service.verify_mongodb_ids(recipe['ingredients']['optional_items'])
                    recipe['ingredients']['optional_items'] = valid_optional_ids
                    
                    # Get the full ingredient details
                    optional_items_details = mongodb_service.get_items_by_mongodb_ids(valid_optional_ids)
                    recipe['ingredients']['optional_items_details'] = optional_items_details
                
                verified_recipes.append(recipe)
    
    return verified_recipes

@api_bp.route('/recipes', methods=['POST'])
def create_recipes():
    """
    POST endpoint to generate recipes based on user preferences
    
    Request body:
    - JSON object containing user preferences
    
    Returns:
    - JSON response with generated recipes
    """
    try:
        # Get preferences from request JSON body
        preferences = request.get_json() or {}
        
        # Generate recipes
        recipes = generate_recipes(preferences)
        
        # Return recipes without verification
        return jsonify(recipes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Keep the GET endpoint for backward compatibility
@api_bp.route('/recipes', methods=['GET'])
def get_recipes():
    """
    GET endpoint to generate recipes based on user preferences (deprecated)
    
    Query parameters:
    - preferences: JSON string containing user preferences
    
    Returns:
    - JSON response with generated recipes
    """
    try:
        preferences = request.args.get('preferences', '{}')
        recipes = generate_recipes(preferences)
        
        # Return recipes without verification
        return jsonify(recipes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
