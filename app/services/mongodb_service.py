"""
MongoDB Service

This module provides functions to interact with the MongoDB catalog database.
"""

import os
from typing import List, Dict, Any, Optional
from pymongo import MongoClient
from pymongo.collection import ObjectId
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MongoDBService:
    """Service to interact with MongoDB catalog database."""
    
    def __init__(self, mongodb_url: str = None, db_name: str = "iimt-hack-q2-2025", collection_name: str = "catalog"):
        """Initialize MongoDB connection."""
        if mongodb_url is None:
            mongodb_url = os.getenv("MONGODB_URL", "mongodb+srv://anupam:iimt@iimt-hack.wuedgxf.mongodb.net/")
        
        self.client = MongoClient(mongodb_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        
        # Test connection
        try:
            self.client.admin.command('ping')
            print("MongoDB connection successful")
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
    
    def _convert_id_to_str(self, items):
        """Convert ObjectId to string in items."""
        if isinstance(items, list):
            for item in items:
                if '_id' in item and isinstance(item['_id'], ObjectId):
                    item['_id'] = str(item['_id'])
            return items
        elif isinstance(items, dict):
            if '_id' in items and isinstance(items['_id'], ObjectId):
                items['_id'] = str(items['_id'])
            return items
        return items
    
    def get_all_categories(self) -> List[str]:
        """Get all unique categories from the catalog."""
        return self.collection.distinct("category")
    
    def get_items_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all items in a specific category."""
        items = list(self.collection.find({"category": category}))
        return self._convert_id_to_str(items)
    
    def search_items(self, query: str) -> List[Dict[str, Any]]:
        """Search for items matching the query."""
        # Case-insensitive search in item_name
        items = list(self.collection.find({"item_name": {"$regex": query, "$options": "i"}}))
        return self._convert_id_to_str(items)
    
    def get_item_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get an item by its ID."""
        item = self.collection.find_one({"item_id": item_id})
        return self._convert_id_to_str(item) if item else None
    
    def get_item_by_mongodb_id(self, mongodb_id: str) -> Optional[Dict[str, Any]]:
        """Get an item by its MongoDB _id."""
        try:
            if not mongodb_id or not ObjectId.is_valid(mongodb_id):
                return None
            item = self.collection.find_one({"_id": ObjectId(mongodb_id)})
            return self._convert_id_to_str(item) if item else None
        except Exception as e:
            print(f"Error getting item by MongoDB ID: {e}")
            return None
    
    def get_items_by_ids(self, item_ids: List[str]) -> List[Dict[str, Any]]:
        """Get multiple items by their IDs."""
        if not item_ids:
            return []
        items = list(self.collection.find({"item_id": {"$in": item_ids}}))
        return self._convert_id_to_str(items)
    
    def get_items_by_mongodb_ids(self, mongodb_ids: List[str]) -> List[Dict[str, Any]]:
        """Get multiple items by their MongoDB _ids."""
        if not mongodb_ids:
            return []
        
        try:
            # Filter out invalid ObjectIds
            valid_ids = []
            for id_str in mongodb_ids:
                if id_str and ObjectId.is_valid(id_str):
                    valid_ids.append(ObjectId(id_str))
                else:
                    print(f"Warning: Invalid MongoDB ID: {id_str}")
            
            if not valid_ids:
                return []
            
            items = list(self.collection.find({"_id": {"$in": valid_ids}}))
            return self._convert_id_to_str(items)
        except Exception as e:
            print(f"Error getting items by MongoDB IDs: {e}")
            return []
    
    def get_available_ingredients(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get available ingredients, optionally filtered by category."""
        query = {}
        if category:
            query["category"] = category
        
        # Get all items with their MongoDB _id
        items = list(self.collection.find(query))
        return self._convert_id_to_str(items)
    
    def get_random_ingredients(self, count: int = 10, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get random ingredients, optionally filtered by category."""
        query = {}
        if category:
            query["category"] = category
        
        # Get random items with their MongoDB _id
        items = list(self.collection.aggregate([
            {"$match": query},
            {"$sample": {"size": count}}
        ]))
        
        return self._convert_id_to_str(items)
    
    def verify_mongodb_ids(self, mongodb_ids: List[str]) -> List[str]:
        """Verify which MongoDB _ids exist in the database and return only valid ones."""
        if not mongodb_ids:
            return []
        
        valid_ids = []
        for id_str in mongodb_ids:
            if id_str and ObjectId.is_valid(id_str):
                # Check if this ID exists in the database
                item = self.collection.find_one({"_id": ObjectId(id_str)})
                if item:
                    valid_ids.append(id_str)
        
        return valid_ids

def get_mongodb_service() -> MongoDBService:
    """Factory function to get a MongoDB service instance."""
    return MongoDBService()
