#!/usr/bin/env python3
"""
Grocery Catalog Analyzer

This script analyzes the generated grocery catalog and provides statistics.
"""

import csv
import collections
from typing import Dict, List, Tuple

def analyze_catalog(filename: str = "grocery_catalog.csv"):
    """Analyze the grocery catalog and print statistics."""
    items_by_category = collections.defaultdict(set)
    packets_by_category = collections.defaultdict(int)
    packet_sizes_by_category = collections.defaultdict(list)
    unique_items = set()
    total_entries = 0
    
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = row['category']
            item_id = row['item_id']
            packet_weight = int(row['packet_weight_grams'])
            
            items_by_category[category].add(item_id)
            unique_items.add(item_id)
            packets_by_category[category] += 1
            packet_sizes_by_category[category].append(packet_weight)
            total_entries += 1
    
    # Calculate average packet sizes per category
    avg_packet_sizes = {
        category: sum(sizes) / len(sizes) 
        for category, sizes in packet_sizes_by_category.items()
    }
    
    # Calculate average packets per item by category
    avg_packets_per_item = {
        category: packets_by_category[category] / len(items)
        for category, items in items_by_category.items()
    }
    
    # Print statistics
    print(f"Total unique items: {len(unique_items)}")
    print(f"Total catalog entries: {total_entries}")
    print("\nItems by Category:")
    for category in sorted(items_by_category.keys()):
        item_count = len(items_by_category[category])
        print(f"  {category}: {item_count} items, {packets_by_category[category]} packets")
        print(f"    Avg packets per item: {avg_packets_per_item[category]:.2f}")
        print(f"    Avg packet weight: {avg_packet_sizes[category]:.2f} grams")
    
    # Find items with most packet variations
    items_with_packet_counts = collections.defaultdict(int)
    item_names = {}
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            items_with_packet_counts[row['item_id']] += 1
            item_names[row['item_id']] = row['item_name']
    
    top_items = sorted(items_with_packet_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    print("\nTop 5 items with most packet variations:")
    for item_id, count in top_items:
        print(f"  {item_id} ({item_names[item_id]}): {count} packet sizes")

if __name__ == "__main__":
    analyze_catalog("grocery_catalog.csv")
