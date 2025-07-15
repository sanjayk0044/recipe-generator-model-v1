#!/usr/bin/env python3
"""
Simple Grocery Catalog Generator

This script generates a catalog of 10,000 grocery items with exactly two packet sizes
(200g and 500g) for each item. The catalog is designed to be easily queried by LLM models
for recipe suggestions.
"""

import csv
import random
from typing import List, Dict

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
PACKET_SIZES = [200, 500]

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
            
            items.append({
                "item_id": item_id,
                "category": category,
                "item_name": item_name,
                "packet_sizes": PACKET_SIZES
            })
            
            item_count += 1
            
    return items

def create_catalog_csv(items: List[Dict], filename: str = "simple_grocery_catalog.csv"):
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
    print("Generating simplified grocery catalog...")
    items = generate_unique_items(10000)
    output_file = "simple_grocery_catalog.csv"
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
            if i == 0 or (i <= 10):
                print(line.strip())
            if i > 10:
                break
    print("...")

if __name__ == "__main__":
    main()
