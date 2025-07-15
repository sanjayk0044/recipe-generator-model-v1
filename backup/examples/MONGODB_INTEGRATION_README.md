# MongoDB Catalog Integration for Recipe Generator API

This guide explains how to set up and test the MongoDB integration for the recipe generator API.

## Overview

The integration allows the Recipe Generator API to:
1. Store grocery catalog data in MongoDB
2. Query MongoDB for available ingredients
3. Enhance LLM prompts with catalog information
4. Validate generated recipes against the catalog

## Installation

### Step 1: Install Required Dependencies

```bash
pip install pandas pymongo google-generativeai python-dotenv
```

### Step 2: Set Up Environment Variables

Create or update your `.env` file with your Google Gemini API key and MongoDB URL:

```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
echo "MONGODB_URL=mongodb+srv://anupam:iimt@iimt-hack.wuedgxf.mongodb.net/" >> .env
```

Replace `your_api_key_here` with your actual Gemini API key.

## Data Preparation and Upload

### Step 1: Generate the Grocery Catalog CSV

```bash
cd /Volumes/workplace/recipe_generator_api
python examples/generate_simple_catalog.py
```

This creates `simple_grocery_catalog.csv` with 10,000 unique grocery items.

### Step 2: Convert CSV to JSON for MongoDB

```bash
python examples/generate_catalog_json.py
```

This creates `catalog_mongodb.json` with pricing information added.

### Step 3: Upload Data to MongoDB

```bash
python examples/upload_to_mongodb.py
```

This uploads the catalog data to MongoDB in the `grocery.catalog` collection.

## Testing

### Step 1: Test MongoDB Integration

```bash
python examples/test_mongodb_integration.py
```

This tests:
1. MongoDB connection and queries
2. Catalog integration service
3. Recipe generation with MongoDB integration (if API key is available)

### Step 2: Run the Full API Server

```bash
python run.py
```

The API will be available at `http://localhost:5000`.

### Step 3: Test the API with a Sample Request

```bash
curl -X POST http://localhost:5000/api/recipes \
  -H "Content-Type: application/json" \
  -d '{"cuisine":"Italian","meal_type":"dinner","cooking_time":"30min","ingredients_to_include":["pasta","tomato","cheese"]}'
```

## MongoDB Structure

The catalog data in MongoDB has the following structure:

```json
{
  "item_id": "F0001",
  "category": "Fruits",
  "item_name": "Sun Harvest Apple",
  "packet_weight_grams": 200,
  "price": 0.99
}
```

## Integration Components

1. **MongoDB Service (`mongodb_service.py`)**:
   - Connects to MongoDB
   - Provides functions to query the catalog

2. **Catalog Integration Service (`catalog_integration.py`)**:
   - Uses MongoDB service to get catalog data
   - Enhances LLM prompts with catalog information
   - Validates recipe ingredients against the catalog

3. **Gemini Service (`gemini_service.py`)**:
   - Uses catalog integration to enhance prompts
   - Validates generated recipes against the catalog

## Troubleshooting

### MongoDB Connection Issues

If you have trouble connecting to MongoDB:

1. Check your MongoDB URL in the `.env` file
2. Ensure your IP address is whitelisted in MongoDB Atlas
3. Verify that the MongoDB service is running

### Missing Dependencies

If you encounter import errors:

```bash
pip install pandas pymongo google-generativeai python-dotenv
```

### API Key Problems

If the Gemini API doesn't work:

1. Check your API key in the `.env` file
2. Verify that your API key has the necessary permissions
3. Check if you've reached your API quota limit

## Additional Scripts

- `generate_simple_catalog.py`: Generates the CSV catalog
- `generate_catalog_json.py`: Converts CSV to JSON with pricing
- `upload_to_mongodb.py`: Uploads JSON data to MongoDB
- `test_mongodb_integration.py`: Tests the MongoDB integration
