import json
import unittest
from unittest.mock import patch
from app import create_app

class TestRecipeAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Sample mock recipe for testing
        self.mock_recipes = [
            {
                "title": "Test Recipe",
                "summary": "This is a test recipe summary.",
                "ingredients": {
                    "necessary_items": ["Ingredient 1", "Ingredient 2"],
                    "optional_items": ["Optional 1"]
                },
                "procedure": "Step 1: Do this. Step 2: Do that.",
                "image": "A delicious plate of food",
                "youtube": "https://www.youtube.com/watch?v=test"
            }
        ]
        
    @patch('app.services.gemini_service.generate_recipes')
    def test_post_recipes_endpoint(self, mock_generate_recipes):
        # Mock the response from the Gemini service
        mock_generate_recipes.return_value = self.mock_recipes
        
        # Test data
        test_preferences = {"cuisine": "Italian", "dietary": "vegetarian"}
        
        # Test the POST API endpoint
        response = self.client.post(
            '/api/recipes',
            json=test_preferences,
            content_type='application/json'
        )
        
        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), self.mock_recipes)
        
        # Verify the mock was called with the correct parameters
        mock_generate_recipes.assert_called_once_with(test_preferences)
        
    @patch('app.services.gemini_service.generate_recipes')
    def test_get_recipes_endpoint(self, mock_generate_recipes):
        # Mock the response from the Gemini service
        mock_generate_recipes.return_value = self.mock_recipes
        
        # Test the GET API endpoint
        response = self.client.get('/api/recipes?preferences={"cuisine":"Italian"}')
        
        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), self.mock_recipes)
        
        # Verify the mock was called with the correct parameters
        mock_generate_recipes.assert_called_once_with('{"cuisine":"Italian"}')
        
    def test_post_recipes_error_handling(self):
        # Test with invalid JSON body
        response = self.client.post(
            '/api/recipes',
            data="invalid-json",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", json.loads(response.data))
        
    def test_get_recipes_error_handling(self):
        # Test with invalid JSON in query parameter
        response = self.client.get('/api/recipes?preferences=invalid-json')
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", json.loads(response.data))

if __name__ == '__main__':
    unittest.main()
