#!/usr/bin/env python3
"""
MongoDB Connection Test

This script tests the connection to MongoDB and verifies that the catalog data is accessible.
"""

import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the path so we can import from the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

def test_mongodb_connection():
    """Test the connection to MongoDB and verify catalog data."""
    try:
        from pymongo import MongoClient
        
        # Get MongoDB URL from environment
        mongodb_url = os.getenv("MONGODB_URL", "mongodb+srv://anupam:iimt@iimt-hack.wuedgxf.mongodb.net/")
        
        print(f"Connecting to MongoDB: {mongodb_url}")
        client = MongoClient(mongodb_url)
        
        # Test connection
        client.admin.command('ping')
        print("MongoDB connection successful!")
        
        # Check database and collection
        db = client["grocery"]
        collection = db["catalog"]
        
        # Count documents
        count = collection.count_documents({})
        print(f"Found {count} documents in grocery.catalog collection")
        
        # Check for different packet weights
        for weight in [100, 250, 500]:
            weight_count = collection.count_documents({"packet_weight_grams": weight})
            print(f"  - {weight}g packets: {weight_count}")
        
        # Get unique categories
        categories = collection.distinct("category")
        print(f"\nFound {len(categories)} categories: {', '.join(categories[:5])}...")
        
        # Get sample document
        sample = collection.find_one()
        if sample:
            print("\nSample document:")
            for key, value in sample.items():
                print(f"  {key}: {value}")
        
        return True
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return False

if __name__ == "__main__":
    print("Testing MongoDB connection...")
    test_mongodb_connection()
