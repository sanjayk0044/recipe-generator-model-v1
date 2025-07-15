#!/usr/bin/env python3
"""
Generate Catalog JSON for MongoDB

This script converts the grocery catalog CSV to JSON format suitable for MongoDB,
adding price information for each item.
"""

import csv
import json
import random
import decimal
from decimal import Decimal
from typing import List, Dict, Any

def generate_price(weight: int, category: str) -> float:
    """Generate a realistic price based on weight and category."""
    # Base price per gram for different categories
    base_prices = {
        "Fruits": 0.005,
        "Vegetables": 0.004,
        "Dairy": 0.008,
        "Bakery": 0.006,
        "Meat": 0.015,
        "Seafood": 0.020,
        "Grains": 0.002,
        "Canned Goods": 0.004,
        "Snacks": 0.010,
        "Beverages": 0.003,
        "Condiments": 0.007,
        "Spices": 0.030,
        "Frozen Foods": 0.008,
        "Baking": 0.006,
        "Herbs": 0.025
    }
    
    # Get base price for category or use average if not found
    base_price = base_prices.get(category, 0.008)
    
    # Calculate raw price
    raw_price = base_price * weight
    
    # Add some randomness (±20%)
    variation = random.uniform(0.8, 1.2)
    price = raw_price * variation
    
    # Add volume discount for larger packages
    if weight > 400:
        price = price * 0.9
    
    # Round to nearest $0.49 or $0.99
    cents = int((price * 100) % 100)
    if cents < 50:
        price = int(price) + 0.49
    else:
        price = int(price) + 0.99
    
    # Ensure minimum price
    if price < 0.99:
        price = 0.99
    
    return round(price, 2)

def csv_to_json(csv_filename: str, json_filename: str):
    """Convert CSV catalog to JSON format for MongoDB."""
    catalog_entries = []
    
    # Read CSV and create JSON entries
    with open(csv_filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_id = row['item_id']
            category = row['category']
            item_name = row['item_name']
            weight = int(row['packet_weight_grams'])
            
            # Generate a price for this item
            price = generate_price(weight, category)
            
            # Create JSON entry
            entry = {
                "item_id": item_id,
                "category": category,
                "item_name": item_name,
                "packet_weight_grams": weight,
                "price": price
            }
            
            catalog_entries.append(entry)
    
    # Write JSON file
    with open(json_filename, 'w') as f:
        json.dump(catalog_entries, f, indent=2)
    
    return catalog_entries

def main():
    """Main function to convert CSV to JSON."""
    print("Converting grocery catalog CSV to JSON for MongoDB...")
    csv_filename = "simple_grocery_catalog.csv"
    json_filename = "catalog_mongodb.json"
    
    catalog_entries = csv_to_json(csv_filename, json_filename)
    
    print(f"Conversion complete! JSON file saved as: {json_filename}")
    print(f"Total entries: {len(catalog_entries)}")
    
    # Print sample entries
    print("\nSample entries:")
    for entry in catalog_entries[:5]:
        print(json.dumps(entry, indent=2))

if __name__ == "__main__":
    main()
