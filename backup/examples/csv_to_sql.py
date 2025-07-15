#!/usr/bin/env python3
"""
CSV to SQL Converter

This script converts the grocery catalog CSV file to SQL insert statements.
"""

import csv
import random
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Set, List

def generate_price(weight: int, category: str) -> Decimal:
    """Generate a realistic price based on weight and category."""
    # Base price per gram for different categories
    base_prices = {
        "Fruits": Decimal('0.005'),
        "Vegetables": Decimal('0.004'),
        "Dairy": Decimal('0.008'),
        "Bakery": Decimal('0.006'),
        "Meat": Decimal('0.015'),
        "Seafood": Decimal('0.020'),
        "Grains": Decimal('0.002'),
        "Canned Goods": Decimal('0.004'),
        "Snacks": Decimal('0.010'),
        "Beverages": Decimal('0.003'),
        "Condiments": Decimal('0.007'),
        "Spices": Decimal('0.030'),
        "Frozen Foods": Decimal('0.008'),
        "Household": Decimal('0.005'),
        "Personal Care": Decimal('0.015')
    }
    
    # Get base price for category or use average if not found
    base_price = base_prices.get(category, Decimal('0.008'))
    
    # Calculate raw price
    raw_price = base_price * Decimal(weight)
    
    # Add some randomness (±20%)
    variation = Decimal(random.uniform(0.8, 1.2))
    price = raw_price * variation
    
    # Add volume discount for larger packages
    if weight > 1000:
        price = price * Decimal('0.9')
    elif weight > 500:
        price = price * Decimal('0.95')
    
    # Round to nearest $0.49 or $0.99
    cents = int((price * 100) % 100)
    if cents < 50:
        price = price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        price = price.quantize(Decimal('1'), rounding=ROUND_HALF_UP) - Decimal('0.01')
    else:
        price = price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        price = price.quantize(Decimal('1'), rounding=ROUND_HALF_UP) - Decimal('0.51')
    
    # Ensure minimum price
    if price < Decimal('0.99'):
        price = Decimal('0.99')
    
    return price

def csv_to_sql(csv_filename: str, sql_filename: str):
    """Convert CSV catalog to SQL insert statements."""
    categories = set()
    items = {}  # item_id -> (category, name)
    packets = []  # (item_id, weight, price)
    
    # Read CSV and collect data
    with open(csv_filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_id = row['item_id']
            category = row['category']
            item_name = row['item_name']
            weight = int(row['packet_weight_grams'])
            
            categories.add(category)
            items[item_id] = (category, item_name)
            
            # Generate a price for this packet
            price = generate_price(weight, category)
            packets.append((item_id, weight, price))
    
    # Write SQL statements
    with open(sql_filename, 'w') as f:
        # Write header
        f.write("-- SQL Insert statements for grocery catalog\n\n")
        
        # Insert categories
        f.write("-- Insert categories\n")
        for category in sorted(categories):
            f.write(f"INSERT INTO categories (category_name) VALUES ('{category}');\n")
        f.write("\n")
        
        # Insert items
        f.write("-- Insert items\n")
        for item_id, (category, item_name) in sorted(items.items()):
            # Escape single quotes in item names
            item_name = item_name.replace("'", "''")
            f.write(f"INSERT INTO items (item_id, category_id, item_name) VALUES ('{item_id}', "
                   f"(SELECT category_id FROM categories WHERE category_name = '{category}'), "
                   f"'{item_name}');\n")
        f.write("\n")
        
        # Insert packet sizes
        f.write("-- Insert packet sizes\n")
        for item_id, weight, price in sorted(packets):
            # Randomly set some items out of stock
            in_stock = "TRUE" if random.random() > 0.1 else "FALSE"
            f.write(f"INSERT INTO packet_sizes (item_id, weight_grams, price, in_stock) VALUES "
                   f"('{item_id}', {weight}, {price}, {in_stock});\n")

def main():
    """Main function to convert CSV to SQL."""
    print("Converting grocery catalog CSV to SQL insert statements...")
    csv_filename = "grocery_catalog.csv"
    sql_filename = "grocery_catalog_inserts.sql"
    csv_to_sql(csv_filename, sql_filename)
    print(f"Conversion complete! SQL insert statements saved to: {sql_filename}")
    
    # Print some statistics from the SQL file
    with open(sql_filename, 'r') as f:
        content = f.read()
        category_count = content.count("INSERT INTO categories")
        item_count = content.count("INSERT INTO items")
        packet_count = content.count("INSERT INTO packet_sizes")
        
        print(f"Generated SQL statements for:")
        print(f"  - {category_count} categories")
        print(f"  - {item_count} items")
        print(f"  - {packet_count} packet sizes")

if __name__ == "__main__":
    main()
