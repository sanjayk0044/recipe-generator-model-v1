"""
Gemini Service

This module handles interactions with Google's Gemini LLM for recipe generation.
"""

import os
import json
from google import genai
from dotenv import load_dotenv
from app.services.catalog_integration import get_integration_service

# Load environment variables
load_dotenv()
client = genai.Client()

# Initialize catalog integration service
try:
    catalog_service = get_integration_service()
    catalog_integration_enabled = True
    print("Catalog integration service initialized successfully")
except Exception as e:
    catalog_integration_enabled = False
    print(f"Warning: Catalog integration service not available: {e}")

def create_prompt(preferences):
    """
    Create a structured prompt for the Gemini model based on user preferences
    
    Args:
        preferences (dict): User preferences for recipe generation
        
    Returns:
        str: Formatted prompt for the Gemini model
    """
    print("preference: ", json.dumps(preferences, indent=2))
    prompt = f"""
    You are a professional chef and recipe creator. Generate 1 unique recipe based on the following preferences:
    {json.dumps(preferences, indent=2)}
    
    For each recipe, provide the following information in a structured JSON format:
    
    1. title: A catchy title for the recipe
    2. summary: A concise summary of the recipe in maximum 100 words
    3. ingredients: A list of ingredients with quantities, separated into:
       - necessary_items: List of essential ingredients with their details (_id, item_name, packet_weight_grams, price, quantity)
       - optional_items: List of optional ingredients with their details (_id, item_name, packet_weight_grams, price, quantity)
    4. procedure: Detailed step-by-step cooking instructions in maximum 500 words with quantity of ingredient to use.
    5. youtube: If you know of a relevant YouTube tutorial for a similar recipe, include the link (or null if not applicable)
    
    CRITICAL INSTRUCTIONS:
    - You will be provided with a catalog of available ingredients with their _id values.
    - The necessary_items and optional_items must ONLY contain ingredients from this catalog.
    - DO NOT invent or generate any _id values.
    - Only use the exact _id strings provided in the catalog.
    - Make sure all ingredients needed for the recipe are available in the catalog.
    - If you can't make a good recipe with the available ingredients, say so rather than making up ingredients.
    - DO NOT include necessary_items_details or optional_items_details fields in your response.
    - Alway include _id, item_name, packet_weight_grams, price, quantity in necessary_items and optional_items.
    - Quantity is number of packets that should be included.
    - Youtube video must be older than atleast 6 months and can be accessable.
    
    Return your response as a valid JSON array with 1 recipe object. Each object should have the structure described above.
    Do not include any explanations or text outside of the JSON structure.
    """
    
    # Enhance prompt with catalog information if integration is enabled
    if catalog_integration_enabled:
        try:
            prompt = catalog_service.enhance_recipe_prompt(prompt, preferences)
            print("Enhanced prompt with catalog data (first 500 chars):")
            print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
        except Exception as e:
            print(f"Warning: Failed to enhance prompt with catalog: {e}")
    else:
        print("Warning: Catalog integration is not enabled. Prompt will not include catalog data.")
    
    return prompt

def parse_gemini_response(response_text):
    """
    Parse the Gemini model response and extract the recipe information
    
    Args:
        response_text (str): Raw response from the Gemini model
        
    Returns:
        list: List of recipe dictionaries
    """
    # Extract JSON from the response
    try:
        # Find JSON content in the response (it might be wrapped in markdown code blocks)
        json_content = response_text
        if "```json" in response_text:
            json_content = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            json_content = response_text.split("```")[1].strip()
            
        recipes = json.loads(json_content)
        return recipes
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse Gemini response as JSON: {str(e)}")

def clean_recipe_response(recipes):
    """
    Clean up the recipe response by removing unnecessary fields
    
    Args:
        recipes (list): List of recipe dictionaries
        
    Returns:
        list: List of cleaned recipe dictionaries
    """
    for recipe in recipes:
        if 'ingredients' in recipe:
            # Remove unnecessary fields
            if 'necessary_items_details' in recipe['ingredients']:
                del recipe['ingredients']['necessary_items_details']
            if 'optional_items_details' in recipe['ingredients']:
                del recipe['ingredients']['optional_items_details']
    
    return recipes

def generate_recipes(preferences_str):
    """
    Generate recipes using the Gemini model based on user preferences
    
    Args:
        preferences_str (str): JSON string containing user preferences
        
    Returns:
        list: List of generated recipes
    """
    try:
        # Parse preferences from JSON string if it's a string
        if isinstance(preferences_str, str):
            preferences = json.loads(preferences_str)
        else:
            preferences = preferences_str
        
        # Create the prompt
        prompt = create_prompt(preferences)
        
        # Generate content using Gemini model
        print("Sending request to Gemini API...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,

        )
        print("Received response from Gemini API", response)
    
        
        # Parse the recipes
        recipes = parse_gemini_response(response.text)
        print(f"Parsed {len(recipes)} recipes from response")
        
        # Clean up the response by removing unnecessary fields
        recipes = clean_recipe_response(recipes)
        print("Cleaned up recipe response")
        
        return recipes
    except Exception as e:
        print(f"Error generating recipes: {e}")
        raise Exception(f"Recipe generation failed: {str(e)}")
