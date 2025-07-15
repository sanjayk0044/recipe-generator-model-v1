import requests
import json

def get_recipes_post(preferences):
    """
    Example function to call the recipe generator API using POST
    
    Args:
        preferences (dict): User preferences for recipe generation
        
    Returns:
        list: List of generated recipes
    """
    # Make the API request with JSON body
    response = requests.post(
        'http://localhost:5000/api/recipes',
        json=preferences  # requests automatically converts dict to JSON
    )
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_recipes_get(preferences):
    """
    Example function to call the recipe generator API using GET (deprecated)
    
    Args:
        preferences (dict): User preferences for recipe generation
        
    Returns:
        list: List of generated recipes
    """
    # Convert preferences to JSON string
    preferences_str = json.dumps(preferences)
    
    # Make the API request
    response = requests.get(
        'http://localhost:5000/api/recipes',
        params={'preferences': preferences_str}
    )
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    # Example preferences
    preferences = {
        "cuisine": "Italian",
        "dietary": "vegetarian",
        "meal_type": "dinner",
        "cooking_time": "30min",
        "ingredients_to_include": ["pasta", "tomatoes"],
        "ingredients_to_avoid": ["mushrooms"]
    }
    
    # Get recipes using POST (recommended)
    print("Using POST endpoint:")
    recipes = get_recipes_post(preferences)
    
    # Print the results
    if recipes:
        print(f"Generated {len(recipes)} recipes:")
        for i, recipe in enumerate(recipes, 1):
            print(f"\n{i}. {recipe['title']}")
            print(f"Summary: {recipe['summary']}")
            print("Necessary ingredients:")
            for ingredient in recipe['ingredients']['necessary_items']:
                print(f"  - {ingredient}")
            print("\nSee the full recipe for more details.")
