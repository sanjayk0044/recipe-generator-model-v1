#!/usr/bin/env python3
"""
Grocery Catalog Generator

This script generates a catalog of grocery items with multiple packet sizes for each item.
The catalog is saved as a CSV file.
"""

import csv
import random
from typing import List, Dict, Tuple

# Common grocery categories and items
CATEGORIES = {
    "Fruits": [
        "Apple", "Banana", "Orange", "Grapes", "Strawberry", "Blueberry", "Mango", 
        "Pineapple", "Watermelon", "Kiwi", "Peach", "Pear", "Cherry", "Plum", "Lemon"
    ],
    "Vegetables": [
        "Carrot", "Broccoli", "Spinach", "Tomato", "Potato", "Onion", "Cucumber", 
        "Bell Pepper", "Lettuce", "Cabbage", "Cauliflower", "Corn", "Peas", "Garlic", "Ginger"
    ],
    "Dairy": [
        "Milk", "Cheese", "Yogurt", "Butter", "Cream", "Sour Cream", "Cottage Cheese", 
        "Cream Cheese", "Ice Cream", "Whipped Cream", "Condensed Milk"
    ],
    "Bakery": [
        "Bread", "Bagel", "Croissant", "Muffin", "Cake", "Cookie", "Donut", 
        "Pastry", "Pie", "Roll", "Baguette", "Tortilla", "Pita"
    ],
    "Meat": [
        "Chicken", "Beef", "Pork", "Lamb", "Turkey", "Sausage", "Bacon", 
        "Ham", "Salami", "Pepperoni", "Ground Meat", "Steak"
    ],
    "Seafood": [
        "Salmon", "Tuna", "Shrimp", "Crab", "Lobster", "Cod", "Tilapia", 
        "Sardines", "Mackerel", "Clams", "Mussels", "Oysters"
    ],
    "Grains": [
        "Rice", "Pasta", "Oats", "Cereal", "Quinoa", "Barley", "Couscous", 
        "Flour", "Bread Crumbs", "Cornmeal", "Bulgur"
    ],
    "Canned Goods": [
        "Beans", "Soup", "Tuna", "Corn", "Tomato Sauce", "Vegetables", "Fruit", 
        "Broth", "Chili", "Olives", "Pickles"
    ],
    "Snacks": [
        "Chips", "Crackers", "Popcorn", "Nuts", "Pretzels", "Granola Bars", 
        "Trail Mix", "Dried Fruit", "Jerky", "Rice Cakes"
    ],
    "Beverages": [
        "Water", "Soda", "Juice", "Coffee", "Tea", "Energy Drink", "Sports Drink", 
        "Milk Alternative", "Hot Chocolate", "Lemonade"
    ],
    "Condiments": [
        "Ketchup", "Mustard", "Mayonnaise", "Salsa", "Hot Sauce", "Soy Sauce", 
        "Vinegar", "Olive Oil", "Cooking Oil", "Honey", "Maple Syrup", "Jam"
    ],
    "Spices": [
        "Salt", "Pepper", "Cinnamon", "Oregano", "Basil", "Cumin", "Paprika", 
        "Thyme", "Rosemary", "Curry Powder", "Chili Powder", "Nutmeg"
    ],
    "Frozen Foods": [
        "Pizza", "Vegetables", "Fruits", "Meals", "Ice Cream", "Waffles", 
        "French Fries", "Fish Sticks", "Chicken Nuggets", "Desserts"
    ],
    "Household": [
        "Paper Towels", "Toilet Paper", "Dish Soap", "Laundry Detergent", "Trash Bags", 
        "Cleaning Spray", "Sponges", "Air Freshener", "Light Bulbs", "Batteries"
    ],
    "Personal Care": [
        "Shampoo", "Conditioner", "Soap", "Toothpaste", "Deodorant", "Lotion", 
        "Sunscreen", "Shaving Cream", "Razors", "Cotton Swabs"
    ]
}

# Common brands for each category
BRANDS = {
    "Fruits": ["Nature's Best", "Fresh Farms", "Organic Valley", "Sun Harvest", "Green Fields"],
    "Vegetables": ["Garden Fresh", "Farm Direct", "Organic Choice", "Valley Greens", "Earth's Bounty"],
    "Dairy": ["Dairy Delight", "Creamy Farms", "Pure Dairy", "Milky Way", "Farm Fresh"],
    "Bakery": ["Golden Crust", "Baker's Delight", "Fresh Bake", "Artisan Bread Co.", "Morning Glory"],
    "Meat": ["Prime Cuts", "Butcher's Choice", "Farm Raised", "Quality Meats", "Premium Select"],
    "Seafood": ["Ocean Fresh", "Sea Delight", "Catch of the Day", "Pacific Choice", "Atlantic Harvest"],
    "Grains": ["Grain Masters", "Wholesome Fields", "Natural Harvest", "Golden Grain", "Earth's Best"],
    "Canned Goods": ["Pantry Staples", "Canned Classics", "Preserved Perfection", "Valley Canning Co.", "Shelf Life"],
    "Snacks": ["Snack Time", "Munch Masters", "Crispy Delights", "Snack Attack", "Nibbles"],
    "Beverages": ["Refreshing Springs", "Thirst Quencher", "Pure Drinks", "Beverage Co.", "Liquid Refreshment"],
    "Condiments": ["Flavor Enhancers", "Taste Makers", "Gourmet Touch", "Chef's Choice", "Flavor Fusion"],
    "Spices": ["Spice World", "Flavor Masters", "Aromatic Spices", "Global Flavors", "Spice Traders"],
    "Frozen Foods": ["Frozen Fresh", "Arctic Delights", "Freeze Frame", "Icy Goodness", "Frost Bites"],
    "Household": ["Home Essentials", "Clean Living", "House Helpers", "Domestic Bliss", "Home Solutions"],
    "Personal Care": ["Body Basics", "Personal Best", "Self Care", "Hygiene Heroes", "Body & Beyond"]
}

# Common packet sizes for different categories (in grams)
PACKET_SIZES = {
    "Fruits": [250, 500, 1000, 2000],
    "Vegetables": [250, 500, 1000, 2000],
    "Dairy": [100, 200, 500, 1000],
    "Bakery": [100, 200, 400, 800],
    "Meat": [250, 500, 750, 1000],
    "Seafood": [200, 400, 600, 800],
    "Grains": [250, 500, 1000, 2000, 5000],
    "Canned Goods": [200, 400, 800],
    "Snacks": [50, 100, 200, 300, 500],
    "Beverages": [250, 500, 1000, 2000],
    "Condiments": [100, 250, 500, 750],
    "Spices": [25, 50, 100, 200],
    "Frozen Foods": [300, 500, 750, 1000],
    "Household": [100, 250, 500, 1000],
    "Personal Care": [50, 100, 200, 400]
}

def generate_item_id(category: str, index: int) -> str:
    """Generate a unique item ID based on category and index."""
    category_code = ''.join([word[0] for word in category.split()]).upper()
    return f"{category_code}{index:04d}"

def generate_unique_items(total_items: int = 10000) -> List[Dict]:
    """Generate a list of unique grocery items."""
    items = []
    item_count = 0
    
    # Calculate items per category
    categories = list(CATEGORIES.keys())
    items_per_category = total_items // len(categories)
    remainder = total_items % len(categories)
    
    for category in categories:
        # Adjust items for this category
        category_items = items_per_category + (1 if remainder > 0 else 0)
        if remainder > 0:
            remainder -= 1
            
        # Generate items for this category
        for i in range(category_items):
            if item_count >= total_items:
                break
                
            # Select a base item name from the category
            base_item = random.choice(CATEGORIES[category])
            brand = random.choice(BRANDS[category])
            
            # Create variations if needed to reach the target number
            variation = ""
            if i >= len(CATEGORIES[category]):
                variation_options = ["Premium", "Organic", "Value", "Special", "Classic", 
                                    "Gold", "Silver", "Deluxe", "Light", "Extra", "Super"]
                variation = f" {random.choice(variation_options)}"
            
            item_name = f"{brand} {base_item}{variation}"
            item_id = generate_item_id(category, i+1)
            
            # Generate 1-4 packet sizes for this item
            num_packets = random.randint(1, 4)
            available_sizes = PACKET_SIZES[category].copy()
            random.shuffle(available_sizes)
            packet_sizes = available_sizes[:num_packets]
            packet_sizes.sort()
            
            items.append({
                "item_id": item_id,
                "category": category,
                "item_name": item_name,
                "packet_sizes": packet_sizes
            })
            
            item_count += 1
            
    return items

def create_catalog_csv(items: List[Dict], filename: str = "grocery_catalog.csv"):
    """Create a CSV file with the grocery catalog."""
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['item_id', 'category', 'item_name', 'packet_weight_grams']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in items:
            for weight in item['packet_sizes']:
                writer.writerow({
                    'item_id': item['item_id'],
                    'category': item['category'],
                    'item_name': item['item_name'],
                    'packet_weight_grams': weight
                })

def main():
    """Main function to generate the grocery catalog."""
    print("Generating grocery catalog...")
    items = generate_unique_items(10000)
    output_file = "grocery_catalog.csv"
    create_catalog_csv(items, output_file)
    print(f"Catalog generated successfully! File saved as: {output_file}")
    
    # Print some statistics
    total_entries = sum(len(item['packet_sizes']) for item in items)
    print(f"Total unique items: {len(items)}")
    print(f"Total catalog entries (including different packet sizes): {total_entries}")
    
    # Sample of the catalog
    print("\nSample entries from the catalog:")
    with open(output_file, 'r') as f:
        for i, line in enumerate(f):
            if i == 0 or (i <= 5):
                print(line.strip())
            if i > 5:
                break
    print("...")

if __name__ == "__main__":
    main()
