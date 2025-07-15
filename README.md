# Recipe Generator API with MongoDB Catalog Integration

A Flask-based API that generates recipe recommendations using Google's Gemini 2.5 Flash AI model based on user preferences and ingredients from a MongoDB grocery catalog.

## Features

- POST API endpoint to generate recipe recommendations
- Integration with Google's Gemini 2.5 Flash AI model
- MongoDB integration for grocery catalog querying
- Structured recipe output including:
  - Recipe title
  - Summary (100 words)
  - Detailed procedure (up to 500 words)
  - Ingredients list with MongoDB _id references
  - YouTube links (when available)

## Setup

### Prerequisites

- Python 3.8+
- Google Gemini API key
- MongoDB database with grocery catalog

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/recipe-generator-api.git
   cd recipe-generator-api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API keys and MongoDB URL:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   MONGODB_URL=mongodb+srv://anupam:iimt@iimt-hack.wuedgxf.mongodb.net/
   ```

## MongoDB Catalog Structure

The grocery catalog in MongoDB should have the following structure:

```json
{
  "_id": "unique_mongodb_id",
  "item_id": "F0001",
  "category": "Fruits",
  "item_name": "Organic Valley Apple",
  "packet_weight_grams": 100,
  "price": 0.99
}
```

Each grocery item has three packet sizes (100g, 250g, 500g), each with its own document and unique _id.

## Project Structure

```
recipe_generator_api/
├── app/
│   ├── __init__.py        # Flask app initialization
│   ├── routes.py          # API endpoints
│   └── services/
│       ├── catalog_integration.py  # Catalog integration with LLM
│       ├── gemini_service.py       # LLM interaction
│       └── mongodb_service.py      # MongoDB connection and queries
├── .env                   # Environment variables
├── Dockerfile             # For containerization
├── README.md              # Documentation
├── requirements.txt       # Dependencies
└── run.py                 # Main entry point
```

## Usage

### Running the API

```
python run.py
```

The API will be available at `http://localhost:5000`.

### API Endpoints

#### POST /api/recipes

Generates recipe recommendations based on user preferences and available ingredients in the catalog.

**Request Body:**

```json
{
  "cuisine": "Italian",
  "dietary": "vegetarian",
  "meal_type": "dinner",
  "cooking_time": "30min",
  "ingredients_to_include": ["pasta", "tomatoes"],
  "ingredients_to_avoid": ["mushrooms"]
}
```

**Example Request:**

```bash
curl -X POST http://localhost:5000/api/recipes \
  -H "Content-Type: application/json" \
  -d '{"cuisine":"Italian","dietary":"vegetarian","meal_type":"dinner","cooking_time":"30min"}'
```

**Example Response:**

```json
[
  {
    "title": "Quick Vegetarian Pasta Primavera",
    "summary": "A light and flavorful pasta dish packed with seasonal vegetables and herbs...",
    "ingredients": {
      "necessary_items": [
        "5f8e7d6c9a1b2c3d4e5f6a7b",
        "6a7b8c9d0e1f2a3b4c5d6e7f",
        "7b8c9d0e1f2a3b4c5d6e7f8a"
      ],
      "necessary_items_details": [
        {
          "_id": "5f8e7d6c9a1b2c3d4e5f6a7b",
          "item_id": "G0001",
          "category": "Grains",
          "item_name": "Grain Masters Pasta",
          "packet_weight_grams": 500,
          "price": 2.99
        },
        {
          "_id": "6a7b8c9d0e1f2a3b4c5d6e7f",
          "item_id": "V0001",
          "category": "Vegetables",
          "item_name": "Garden Fresh Bell Pepper",
          "packet_weight_grams": 250,
          "price": 1.49
        },
        {
          "_id": "7b8c9d0e1f2a3b4c5d6e7f8a",
          "item_id": "V0002",
          "category": "Vegetables",
          "item_name": "Earth's Bounty Zucchini",
          "packet_weight_grams": 500,
          "price": 2.49
        }
      ],
      "optional_items": [
        "8c9d0e1f2a3b4c5d6e7f8a9b",
        "9d0e1f2a3b4c5d6e7f8a9b0c"
      ],
      "optional_items_details": [
        {
          "_id": "8c9d0e1f2a3b4c5d6e7f8a9b",
          "item_id": "S0001",
          "category": "Spices",
          "item_name": "Spice World Red Pepper Flakes",
          "packet_weight_grams": 100,
          "price": 1.99
        },
        {
          "_id": "9d0e1f2a3b4c5d6e7f8a9b0c",
          "item_id": "S0002",
          "category": "Snacks",
          "item_name": "Snack Attack Pine Nuts",
          "packet_weight_grams": 250,
          "price": 4.99
        }
      ]
    },
    "procedure": "1. Bring a large pot of salted water to a boil...",
    "youtube": "https://www.youtube.com/watch?v=example"
  }
]
```

#### GET /api/recipes (Legacy)

Legacy endpoint that accepts preferences as a query parameter.

**Example Request:**

```
GET /api/recipes?preferences={"cuisine":"Italian","dietary":"vegetarian","meal_type":"dinner","cooking_time":"30min"}
```

## Docker Deployment

Build and run the Docker container:

```bash
docker build -t recipe-generator-api .
docker run -p 5000:5000 -e GEMINI_API_KEY=your_key_here -e MONGODB_URL=your_mongodb_url recipe-generator-api
```

## License

MIT
