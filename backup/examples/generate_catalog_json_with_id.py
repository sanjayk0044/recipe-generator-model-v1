#!/usr/bin/env python3
"""
Generate Catalog JSON for MongoDB with Unique _id

This script generates a JSON file with grocery catalog data suitable for MongoDB,
including unique _id fields and three packet weights (100g, 250g, 500g) for each item.
"""

import json
import random
import uuid
from typing import List, Dict, Any

# Common grocery categories and items
CATEGORIES = {
    "Fruits": [
        "Apple", "Banana", "Orange", "Grapes", "Strawberry", "Blueberry", "Mango", 
        "Pineapple", "Watermelon", "Kiwi", "Peach", "Pear", "Cherry", "Plum", "Lemon",
        "Lime", "Raspberry", "Blackberry", "Apricot", "Coconut", "Pomegranate", "Fig",
        "Guava", "Papaya", "Passion Fruit", "Dragon Fruit", "Lychee", "Avocado"
    ],
    "Vegetables": [
        "Carrot", "Broccoli", "Spinach", "Tomato", "Potato", "Onion", "Cucumber", 
        "Bell Pepper", "Lettuce", "Cabbage", "Cauliflower", "Corn", "Peas", "Garlic", "Ginger",
        "Zucchini", "Eggplant", "Asparagus", "Celery", "Radish", "Beetroot", "Kale",
        "Brussels Sprouts", "Artichoke", "Leek", "Turnip", "Sweet Potato", "Pumpkin",
        "Squash", "Okra", "Green Beans", "Mushroom", "Bok Choy", "Arugula"
    ],
    "Dairy": [
        "Milk", "Cheese", "Yogurt", "Butter", "Cream", "Sour Cream", "Cottage Cheese", 
        "Cream Cheese", "Ice Cream", "Whipped Cream", "Condensed Milk", "Buttermilk",
        "Ghee", "Paneer", "Ricotta", "Mozzarella", "Cheddar", "Parmesan", "Feta",
        "Gouda", "Brie", "Camembert", "Blue Cheese", "Swiss Cheese", "Mascarpone"
    ],
    "Bakery": [
        "Bread", "Bagel", "Croissant", "Muffin", "Cake", "Cookie", "Donut", 
        "Pastry", "Pie", "Roll", "Baguette", "Tortilla", "Pita", "Naan", "Focaccia",
        "Brioche", "Sourdough", "Rye Bread", "Ciabatta", "Pretzel", "Scone", "Biscuit",
        "Pancake Mix", "Waffle Mix", "Brownie Mix", "Cupcake", "Danish", "Cinnamon Roll"
    ],
    "Meat": [
        "Chicken", "Beef", "Pork", "Lamb", "Turkey", "Sausage", "Bacon", 
        "Ham", "Salami", "Pepperoni", "Ground Meat", "Steak", "Ribs", "Brisket",
        "Veal", "Duck", "Venison", "Rabbit", "Goat", "Liver", "Chicken Wings",
        "Chicken Breast", "Chicken Thigh", "Beef Sirloin", "Beef Tenderloin",
        "Pork Chop", "Pork Belly", "Lamb Chop", "Meatballs"
    ],
    "Seafood": [
        "Salmon", "Tuna", "Shrimp", "Crab", "Lobster", "Cod", "Tilapia", 
        "Sardines", "Mackerel", "Clams", "Mussels", "Oysters", "Squid", "Octopus",
        "Scallops", "Trout", "Halibut", "Sea Bass", "Catfish", "Haddock", "Flounder",
        "Snapper", "Swordfish", "Anchovies", "Caviar", "Fish Sticks", "Fish Fillet"
    ],
    "Grains": [
        "Rice", "Pasta", "Oats", "Cereal", "Quinoa", "Barley", "Couscous", 
        "Flour", "Bread Crumbs", "Cornmeal", "Bulgur", "Farro", "Millet", "Buckwheat",
        "Polenta", "Semolina", "Wheat Germ", "Wheat Bran", "Corn Flour", "Rice Flour",
        "Almond Flour", "Coconut Flour", "Rye Flour", "Whole Wheat Flour", "Pasta Shells",
        "Spaghetti", "Penne", "Macaroni", "Lasagna", "Noodles", "Vermicelli"
    ],
    "Canned Goods": [
        "Beans", "Soup", "Tuna", "Corn", "Tomato Sauce", "Vegetables", "Fruit", 
        "Broth", "Chili", "Olives", "Pickles", "Sardines", "Salmon", "Chicken",
        "Beef Stew", "Peas", "Carrots", "Mushrooms", "Pumpkin", "Coconut Milk",
        "Condensed Milk", "Evaporated Milk", "Tomato Paste", "Salsa", "Spaghetti Sauce"
    ],
    "Snacks": [
        "Chips", "Crackers", "Popcorn", "Nuts", "Pretzels", "Granola Bars", 
        "Trail Mix", "Dried Fruit", "Jerky", "Rice Cakes", "Cookies", "Chocolate",
        "Candy", "Gum", "Protein Bars", "Fruit Snacks", "Cheese Puffs", "Tortilla Chips",
        "Potato Chips", "Corn Chips", "Peanuts", "Almonds", "Cashews", "Pistachios",
        "Walnuts", "Sunflower Seeds", "Pumpkin Seeds", "Raisins", "Dried Apricots"
    ],
    "Beverages": [
        "Water", "Soda", "Juice", "Coffee", "Tea", "Energy Drink", "Sports Drink", 
        "Milk Alternative", "Hot Chocolate", "Lemonade", "Iced Tea", "Smoothie",
        "Protein Shake", "Coconut Water", "Almond Milk", "Soy Milk", "Oat Milk",
        "Rice Milk", "Apple Juice", "Orange Juice", "Grape Juice", "Cranberry Juice",
        "Tomato Juice", "Vegetable Juice", "Beer", "Wine", "Spirits", "Kombucha"
    ],
    "Condiments": [
        "Ketchup", "Mustard", "Mayonnaise", "Salsa", "Hot Sauce", "Soy Sauce", 
        "Vinegar", "Olive Oil", "Cooking Oil", "Honey", "Maple Syrup", "Jam",
        "Jelly", "Peanut Butter", "Almond Butter", "Nutella", "BBQ Sauce", "Teriyaki Sauce",
        "Worcestershire Sauce", "Fish Sauce", "Oyster Sauce", "Hoisin Sauce", "Sriracha",
        "Tabasco", "Ranch Dressing", "Italian Dressing", "Caesar Dressing", "Aioli"
    ],
    "Spices": [
        "Salt", "Pepper", "Cinnamon", "Oregano", "Basil", "Cumin", "Paprika", 
        "Thyme", "Rosemary", "Curry Powder", "Chili Powder", "Nutmeg", "Garlic Powder",
        "Onion Powder", "Ginger Powder", "Turmeric", "Cardamom", "Cloves", "Allspice",
        "Bay Leaves", "Sage", "Dill", "Mint", "Coriander", "Fennel Seeds", "Mustard Seeds",
        "Saffron", "Vanilla Extract", "Almond Extract", "Cayenne Pepper", "Red Pepper Flakes"
    ],
    "Frozen Foods": [
        "Pizza", "Vegetables", "Fruits", "Meals", "Ice Cream", "Waffles", 
        "French Fries", "Fish Sticks", "Chicken Nuggets", "Desserts", "Burritos",
        "Lasagna", "Pot Pie", "Meatballs", "Dumplings", "Spring Rolls", "Samosas",
        "Garlic Bread", "Breakfast Sandwiches", "Pancakes", "Popsicles", "Frozen Yogurt",
        "Sorbet", "Frozen Berries", "Frozen Spinach", "Frozen Corn", "Frozen Peas"
    ],
    "Baking": [
        "Sugar", "Flour", "Baking Powder", "Baking Soda", "Yeast", "Chocolate Chips",
        "Cocoa Powder", "Vanilla Extract", "Food Coloring", "Sprinkles", "Frosting",
        "Cake Mix", "Brownie Mix", "Cookie Mix", "Pie Crust", "Cornstarch", "Molasses",
        "Brown Sugar", "Powdered Sugar", "Shortening", "Corn Syrup", "Marshmallows",
        "Gelatin", "Pudding Mix", "Pie Filling", "Muffin Mix", "Pancake Mix"
    ],
    "Herbs": [
        "Basil", "Parsley", "Cilantro", "Mint", "Rosemary", "Thyme", "Oregano",
        "Sage", "Dill", "Chives", "Tarragon", "Bay Leaves", "Lemongrass", "Marjoram",
        "Lavender", "Fennel", "Chamomile", "Peppermint", "Spearmint", "Stevia",
        "Curry Leaves", "Kaffir Lime Leaves", "Fenugreek", "Savory", "Sorrel"
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
    "Baking": ["Baker's Choice", "Sweet Essentials", "Cake Craft", "Baking Buddy", "Dessert Master"],
    "Herbs": ["Herbal Essence", "Fresh Herbs", "Green Garden", "Herb Haven", "Nature's Flavors"]
}

# Fixed packet sizes for all items
PACKET_SIZES = [100, 250, 500]

def generate_item_id(category: str, index: int) -> str:
    """Generate a unique item ID based on category and index."""
    category_code = ''.join([word[0] for word in category.split()]).upper()
    return f"{category_code}{index:04d}"

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
    elif weight > 200:
        price = price * 0.95
    
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

def generate_catalog_json(total_items: int = 10000, output_file: str = "catalog_mongodb_with_id.json"):
    """Generate a JSON file with grocery catalog data."""
    catalog_entries = []
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
            base_items = CATEGORIES[category]
            # If we need more items than available in the base list, we'll create variations
            if i < len(base_items):
                base_item = base_items[i]
            else:
                # Create variations by combining with adjectives or using different forms
                base_item = base_items[i % len(base_items)]
                variations = ["Premium", "Organic", "Value", "Special", "Classic", 
                             "Gold", "Silver", "Deluxe", "Light", "Extra", "Super",
                             "Fresh", "Natural", "Pure", "Wild", "Gourmet", "Artisan",
                             "Homestyle", "Traditional", "Original", "Signature"]
                base_item = f"{random.choice(variations)} {base_item}"
            
            brand = random.choice(BRANDS[category])
            item_name = f"{brand} {base_item}"
            item_id = generate_item_id(category, i+1)
            
            # Create entries for each packet size
            for weight in PACKET_SIZES:
                # Generate a unique _id (MongoDB ObjectId is 24 hex characters)
                _id = str(uuid.uuid4()).replace("-", "")[:24]
                
                # Generate price
                price = generate_price(weight, category)
                
                # Create entry
                entry = {
                    "_id": _id,
                    "item_id": item_id,
                    "category": category,
                    "item_name": item_name,
                    "packet_weight_grams": weight,
                    "price": price
                }
                
                catalog_entries.append(entry)
            
            item_count += 1
            if item_count % 1000 == 0:
                print(f"Generated {item_count} items ({len(catalog_entries)} entries)...")
    
    # Write to JSON file
    with open(output_file, 'w') as f:
        json.dump(catalog_entries, f, indent=2)
    
    print(f"Generated {item_count} unique items with {len(catalog_entries)} total entries")
    return catalog_entries

def main():
    """Main function to generate the catalog JSON."""
    print("Generating grocery catalog JSON with unique _id and three packet weights...")
    output_file = "catalog_mongodb_with_id.json"
    
    catalog_entries = generate_catalog_json(10000, output_file)
    
    print(f"Catalog generated successfully! File saved as: {output_file}")
    print(f"Total unique items: {len(catalog_entries) // 3}")
    print(f"Total catalog entries: {len(catalog_entries)}")
    
    # Print sample entries
    print("\nSample entries:")
    for entry in catalog_entries[:3]:
        print(json.dumps(entry, indent=2))

if __name__ == "__main__":
    main()
