#!/usr/bin/env python3
"""
Upload Catalog with ID to MongoDB

This script uploads the grocery catalog JSON data with unique _id to MongoDB.
"""

import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def upload_to_mongodb(json_filename: str, mongodb_url: str, db_name: str, collection_name: str):
    """Upload JSON data to MongoDB."""
    # Load JSON data
    with open(json_filename, 'r') as f:
        catalog_data = json.load(f)
    
    # Connect to MongoDB
    client = MongoClient(mongodb_url)
    db = client[db_name]
    collection = db[collection_name]
    
    # Drop existing collection to start fresh
    collection.drop()
    
    # Insert data
    if len(catalog_data) > 0:
        result = collection.insert_many(catalog_data)
        print(f"Inserted {len(result.inserted_ids)} documents into MongoDB")
    else:
        print("No data to insert")
    
    # Create indexes for better performance
    collection.create_index("item_id")
    collection.create_index("category")
    collection.create_index("item_name")
    collection.create_index("packet_weight_grams")
    
    # Verify the upload
    count = collection.count_documents({})
    print(f"Total documents in collection: {count}")
    
    # Sample query
    sample = list(collection.find().limit(1))
    print("\nSample document:")
    print(json.dumps(sample[0], default=str, indent=2))
    
    # Count unique items
    unique_items = collection.distinct("item_id")
    print(f"\nUnique item_id count: {len(unique_items)}")
    
    # Count by packet weight
    for weight in [100, 250, 500]:
        count = collection.count_documents({"packet_weight_grams": weight})
        print(f"Items with {weight}g packets: {count}")

def main():
    """Main function to upload data to MongoDB."""
    # MongoDB connection details
    mongodb_url = "mongodb+srv://anupam:iimt@iimt-hack.wuedgxf.mongodb.net/"
    db_name = "grocery"
    collection_name = "catalog"
    
    json_filename = "catalog_mongodb_with_id.json"
    
    print(f"Uploading catalog data to MongoDB ({mongodb_url})...")
    upload_to_mongodb(json_filename, mongodb_url, db_name, collection_name)
    print("Upload complete!")

if __name__ == "__main__":
    main()
