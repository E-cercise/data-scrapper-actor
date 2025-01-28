import re
import json
import random

def parse_variant_name(name):
    """
    Parse color and weight from the variant name.
    """
    # Default values
    color = None
    weight = 0.0

    # Regex for weight (e.g., "20kg", "15 lbs")
    weight_regex = re.compile(r'(\d+\.?\d*)\s?(kg|lbs)', re.IGNORECASE)
    weight_match = weight_regex.search(name)
    if weight_match:
        weight = float(weight_match.group(1))
        if weight_match.group(2).lower() == "lbs":
            weight *= 0.453592  # Convert pounds to kilograms

    # Extract color by checking known color keywords
    color_keywords = ["red", "blue", "yellow", "green", "orange", "purple", "white", "black", "gray",
		"silver", "beige", "cream", "brown", "tan", "pink", "light blue", "dark blue",
		"light green", "dark green", "navy", "maroon", "olive", "teal", "turquoise",
		"lavender", "violet", "indigo", "gold", "bronze", "copper", "chrome", "cyan",
		"magenta", "peach", "mint", "coral", "burgundy", "ivory", "aqua", "rose",
		"charcoal", "salmon", "mustard", "lime"]

    name_lower = name.lower()
    for keyword in color_keywords:
        if keyword in name_lower:
            color = keyword.title()  # Capitalize the first letter
            break

    return color, weight

def value_of_attribute(attr: list[dict], key: str):
    for att in attr:
        if att["key"] == key:
            return att["value"]
    return None

def process_variant_data(json_file):
    """
    Read the JSON file and process each variant.
    """
    # Load the JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Results list to hold the processed equipment options


    for product in data:
        product["equipment_options"] = []

        variants = product.get("variantDetails", [])
        
        weight = value_of_attribute(product["attributes"], "Item Weight")
        if weight == None:
            continue
        
        color = value_of_attribute(product["attributes"], "Color")
        if color == None:
            continue
        price = product["price"]

    
        if len(variants) == 0:
            product["equipment_options"] = {
                "weight": weight,
                "price": price,
                "remaining_products": random.randint(0, 101),
                "color": color
            }
        for variant in variants:
            name = variant.get("name", "")
            price = variant.get("price", {})

            if price == None:
                price = product["price"]
            else:
                price = price.get("value", 0.0)
            # Parse color and weight
            color, weight = parse_variant_name(name)

            # Create an EquipmentOption dictionary
            equipment_option = {
                "weight": weight,
                "price": price,
                "remaining_products": random.randint(0, 101),
                "color": color
            }

            # Append the processed equipment option
            product["equipment_options"].append(equipment_option)
            
        
    return data
        
if __name__ == "__main__":
    # Replace with the path to your JSON file
    json_file = "clean1/assited_pull_up_machine_unique_clean.json"

    # Process the JSON file
    processed_data = process_variant_data(json_file)


    # Optionally save the processed data to a new JSON file
    with open("processed_equipment_options.json", "w") as outfile:
        json.dump(processed_data, outfile, indent=4)
