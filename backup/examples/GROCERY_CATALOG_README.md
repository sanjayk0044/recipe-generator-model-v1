# Grocery Catalog Generator

This directory contains scripts to generate a comprehensive grocery catalog for a store with 10,000 items, where each item can have multiple packet sizes.

## Files

- `generate_grocery_catalog.py`: Main script to generate the grocery catalog CSV file
- `analyze_catalog.py`: Script to analyze the generated catalog and provide statistics
- `csv_to_sql.py`: Script to convert the CSV catalog to SQL insert statements
- `grocery_catalog_schema.sql`: SQL schema for the grocery catalog database
- `grocery_catalog.csv`: Generated CSV file containing the grocery catalog
- `grocery_catalog_inserts.sql`: Generated SQL insert statements for the catalog

## Catalog Structure

The grocery catalog is structured as follows:

- **Item ID**: A unique identifier for each grocery item (e.g., F0001 for Fruits)
- **Category**: The category the item belongs to (e.g., Fruits, Vegetables, Dairy)
- **Item Name**: The name of the item, including brand (e.g., Fresh Farms Watermelon)
- **Packet Weight**: The weight of each packet in grams
- **Price**: The price of each packet (in the SQL version)
- **In Stock**: Whether the packet is in stock (in the SQL version)

Each item can have multiple packet sizes, typically ranging from 1 to 4 different weights.

## Database Schema

The SQL schema consists of three main tables:

1. **categories**: Stores the grocery categories
   - category_id (PK)
   - category_name

2. **items**: Stores the grocery items
   - item_id (PK)
   - category_id (FK)
   - item_name
   - created_at
   - updated_at

3. **packet_sizes**: Stores the different packet sizes for each item
   - packet_id (PK)
   - item_id (FK)
   - weight_grams
   - price
   - in_stock
   - created_at
   - updated_at

## Usage

### Generating the Catalog

```bash
python generate_grocery_catalog.py
```

This will create a CSV file named `grocery_catalog.csv` with approximately 25,000 entries (10,000 unique items with multiple packet sizes).

### Analyzing the Catalog

```bash
python analyze_catalog.py
```

This will provide statistics about the generated catalog, including:
- Total unique items
- Total catalog entries
- Items by category
- Average packets per item
- Average packet weight by category
- Top items with most packet variations

### Converting to SQL

```bash
python csv_to_sql.py
```

This will convert the CSV catalog to SQL insert statements in a file named `grocery_catalog_inserts.sql`.

## Statistics

The generated catalog has the following characteristics:

- **Total unique items**: 8,000
- **Total catalog entries**: ~25,000
- **Categories**: 15
- **Average packets per item**: ~2.5
- **Average packet weight**: Varies by category (e.g., Spices: ~94g, Grains: ~1,700g)

## Example Entries

```
item_id,category,item_name,packet_weight_grams
F0001,Fruits,Fresh Farms Watermelon,500
F0001,Fruits,Fresh Farms Watermelon,1000
F0002,Fruits,Sun Harvest Plum,1000
F0003,Fruits,Fresh Farms Banana,1000
F0004,Fruits,Fresh Farms Lemon,250
```

## Database Usage Examples

Once the database is set up with the schema and insert statements, you can use the following queries:

### Get all packet sizes for a specific item

```sql
SELECT * FROM get_item_packets('F0001');
```

### Search for items by name

```sql
SELECT * FROM search_items('Watermelon');
```

### Get all items in a specific category

```sql
SELECT i.item_id, i.item_name, COUNT(ps.packet_id) as packet_count
FROM items i
JOIN categories c ON i.category_id = c.category_id
JOIN packet_sizes ps ON i.item_id = ps.item_id
WHERE c.category_name = 'Fruits'
GROUP BY i.item_id, i.item_name
ORDER BY i.item_name;
```

### Get all available packet sizes for a specific category

```sql
SELECT DISTINCT ps.weight_grams
FROM packet_sizes ps
JOIN items i ON ps.item_id = i.item_id
JOIN categories c ON i.category_id = c.category_id
WHERE c.category_name = 'Fruits'
ORDER BY ps.weight_grams;
```
