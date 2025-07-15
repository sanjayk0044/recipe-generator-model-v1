# Grocery Catalog Integration for Recipe Generator API

This integration allows the Recipe Generator API to suggest recipes based on ingredients available in a grocery catalog. The LLM model can query the catalog and recommend recipes using only the ingredients found in the catalog.

## Files

- `simple_grocery_catalog.csv`: CSV file containing 10,000 grocery items with 200g and 500g packet sizes
- `generate_simple_catalog.py`: Script to generate the grocery catalog
- `recipe_ingredient_matcher.py`: Standalone script to match recipe ingredients with catalog items
- `test_catalog_recipes.py`: Test script for the catalog-integrated recipe generator
- `../app/services/catalog_integration.py`: Service that integrates the catalog with the recipe generator API

## Catalog Structure

The grocery catalog has a simple structure:

- **item_id**: Unique identifier for each item (e.g., F0001 for Fruits)
- **category**: The category the item belongs to (e.g., Fruits, Vegetables, Dairy)
- **item_name**: The name of the item, including brand (e.g., Fresh Farms Apple)
- **packet_weight_grams**: The weight of each packet (200g or 500g)

Each item has exactly two packet sizes: 200g and 500g.

## Integration Features

1. **Enhanced Prompts**: The integration enhances the prompts sent to the LLM by including relevant ingredients from the catalog based on the user's preferences.

2. **Ingredient Validation**: After receiving recipes from the LLM, the integration validates the ingredients against the catalog and replaces generic ingredients with specific catalog items.

3. **Ingredient Search**: The integration allows searching for ingredients in the catalog, making it easy to find available items.

4. **Category Filtering**: You can filter ingredients by category to focus on specific types of food.

## Usage

### Generating a Catalog

```bash
python generate_simple_catalog.py
```

This will create a CSV file named `simple_grocery_catalog.csv` with 10,000 unique items, each with 200g and 500g packet sizes.

### Testing the Integration

```bash
python test_catalog_recipes.py
```

This script demonstrates how the catalog integration works with the recipe generator API by:
1. Searching for ingredients in the catalog
2. Enhancing the prompt with catalog information
3. Generating recipes using the Gemini API
4. Validating the ingredients against the catalog

### Using the Integration in Your Code

```python
from app.services.gemini_service import generate_recipes
from app.services.catalog_integration import get_integration_service

# Initialize catalog service
catalog_service = get_integration_service()

# Search for ingredients
results = catalog_service.search_ingredients("chicken")

# Generate recipe with catalog integration
preferences = {
    "cuisine": "Italian",
    "meal_type": "dinner",
    "cooking_time": "30min",
    "ingredients_to_include": ["pasta", "tomato", "cheese"]
}

recipes = generate_recipes(preferences)
```

## API Integration

The catalog integration is automatically used by the Recipe Generator API. When you make a request to the API, it will:

1. Search for the requested ingredients in the catalog
2. Enhance the prompt with relevant catalog items
3. Validate the generated recipes against the catalog

### Example API Request

```bash
curl -X POST http://localhost:5000/api/recipes \
  -H "Content-Type: application/json" \
  -d '{"cuisine":"Italian","meal_type":"dinner","cooking_time":"30min","ingredients_to_include":["pasta","tomato","cheese"]}'
```

## Customizing the Catalog

You can customize the catalog by modifying the `generate_simple_catalog.py` script:

- Add or remove categories
- Change the list of items in each category
- Add more brands
- Modify the packet sizes

After making changes, regenerate the catalog by running the script.

## Limitations

1. The current implementation only supports exact or partial string matching for ingredients.
2. The integration doesn't handle quantities or units conversion.
3. The catalog doesn't include pricing information.

## Future Improvements

1. Add semantic matching for ingredients (e.g., "beef" should match "ground beef")
2. Include pricing information for cost estimation
3. Add nutritional information for dietary recommendations
4. Implement inventory tracking to suggest recipes based on what's in stock
