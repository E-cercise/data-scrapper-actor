import os
import re
import json
import random

def parse_weight_string(weight_str):
    """
    Parse a string like '23.14 Pounds', '50 lbs', '10 kg', etc.
    Return a float in kilograms. Return 0.0 if parsing fails.
    """

    # If weight_str is already a numeric type, just convert to float
    if isinstance(weight_str, (int, float)):
        return float(weight_str)

    # Known unit synonyms
    weight_unit_synonyms = {
        "kg": "kg",
        "kilos": "kg",
        "kilograms": "kg",
        "lbs": "lbs",
        "lb": "lbs",
        "pounds": "lbs",
        "pound": "lbs"
    }

    weight_regex = re.compile(
        r'(\d+(?:\.\d+)?)\s?(kg|kilos|kilograms|lbs|lb|pounds|pound)',
        re.IGNORECASE
    )
    match = weight_regex.search(weight_str)
    if match:
        raw_number = match.group(1)       # e.g. "23.14" 
        raw_unit = match.group(2).lower() # e.g. "pounds"

        try:
            parsed_weight = float(raw_number)
        except ValueError:
            return 0.0

        # Convert synonyms to either "kg" or "lbs"
        standard_unit = weight_unit_synonyms.get(raw_unit, None)

        if standard_unit == "kg":
            return parsed_weight
        elif standard_unit == "lbs":
            return parsed_weight * 0.453592  # lbs -> kg
        else:
            # If not recognized, just treat the number as-is
            return parsed_weight
    else:
        # If no match, try just converting directly if it's purely numeric
        try:
            return float(weight_str)
        except ValueError:
            return 0.0

def parse_variant_name(name):
    """
    Parse color and weight from the variant name.
    """
    color = None
    weight = 0.0

    # Define unit synonyms
    # For each key in this dict, the value tells us the 'standard' unit to treat it as
    weight_unit_synonyms = {
        "kg": "kg",
        "kilos": "kg",
        "kilograms": "kg",
        "lbs": "lbs",
        "lb": "lbs",
        "pounds": "lbs",
        "pound": "lbs",
    }

    # Build a more inclusive regex pattern
    # (\d+(\.\d+)?): one or more digits, optional decimal, optional more digits
    # \s?: optional whitespace
    # (kg|lbs|pounds|pound|lb|...): the unit synonyms
    # re.IGNORECASE so it matches uppercase or mixed case forms
    weight_regex = re.compile(
        r"(\d+(?:\.\d+)?)\s?(kg|kilos|kilograms|lbs|lb|pounds|pound)", re.IGNORECASE
    )

    match = weight_regex.search(name)
    if match:
        raw_number = match.group(1)  # e.g. "89" in "89 Pounds"
        raw_unit = match.group(2).lower()  # e.g. "pounds"

        try:
            parsed_weight = float(raw_number)
        except ValueError:
            parsed_weight = 0.0

        # Convert to "kg" or "lbs" using synonyms
        standard_unit = weight_unit_synonyms.get(raw_unit, None)

        if standard_unit == "kg":
            weight = parsed_weight
        elif standard_unit == "lbs":
            # Convert from pounds to kilograms
            weight = parsed_weight * 0.453592
        else:
            weight = (
                parsed_weight  # If we don't recognize the unit, just store the float.
            )

    # Extract color by checking known color keywords
    color_keywords = [
        "red",
        "blue",
        "yellow",
        "green",
        "orange",
        "purple",
        "white",
        "black",
        "gray",
        "silver",
        "beige",
        "cream",
        "brown",
        "tan",
        "pink",
        "light blue",
        "dark blue",
        "light green",
        "dark green",
        "navy",
        "maroon",
        "olive",
        "teal",
        "turquoise",
        "lavender",
        "violet",
        "indigo",
        "gold",
        "bronze",
        "copper",
        "chrome",
        "cyan",
        "magenta",
        "peach",
        "mint",
        "coral",
        "burgundy",
        "ivory",
        "aqua",
        "rose",
        "charcoal",
        "salmon",
        "mustard",
        "lime",
    ]
    color_list = []
    name_lower = name.lower()
    for keyword in color_keywords:
        if keyword in name_lower:
            color_list.append(keyword.title())  

    color = ", ".join(color_list)

    return color, weight


def value_of_attribute(attr_list, key: str):
    for att in attr_list:
        if att.get("key") == key:
            return att.get("value")
    return None


def process_variant_data(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)
        
    new_data = []

    for product in data:
        product["equipment_options"] = []

        # Gather product-level attributes
        variants = product.get("variantDetails", [])

        item_weight = value_of_attribute(product["attributes"], "Item Weight")
        item_color = value_of_attribute(product["attributes"], "Color")
        base_price = product.get("price", 0.0)


        # Skip products missing top-level weight or color
        if item_weight is None or item_color is None:
            continue

        # If there are no variants, create a single option
        if not variants: 
            img_list = [{"link": product["thumbnailImage"], "is_primary": True}] + [{"link": img_link, "is_primary": False} for img_link in product["galleryThumbnails"]]
            product["equipment_options"].append(
                {
                    "name": f"Item {item_weight} {base_price}",
                    "weight": item_weight,
                    "price": base_price,
                    "remaining_products": random.randint(0, 101),
                    "color": item_color,
                    "img": img_list
                }
            )
        else:
            # Parse each variant
            for variant in variants:
                variant_name = variant.get("name", "")
                variant_price_struct = variant.get("price", {})

                if variant_price_struct == None:
                    variant_price = product["price"]
                else:
                    variant_price = variant_price_struct.get("value", base_price)

                parsed_color, parsed_weight = parse_variant_name(variant_name)

                # Fallbacks if parsing didn't work
                final_color = parsed_color if parsed_color else item_color
                try:
                    fallback_weight = parse_weight_string(item_weight)
                except ValueError as e:
                    print(e)
                    continue
                final_weight = (
                    parsed_weight if parsed_weight != 0.0 else fallback_weight
                )
                
                img_list = [{"link": variant["thumbnail"], "is_primary": True}] + [{"link": img_link, "is_primary": False} for img_link in variant["images"]]

                equipment_option = {
                    "name": variant_name,
                    "weight": final_weight,
                    "price": variant_price,
                    "remaining_products": random.randint(0, 101),
                    "color": final_color,
                    "img": img_list
                }
                product["equipment_options"].append(equipment_option)


        del product["variantDetails"], product["variantAttributes"], product["thumbnailImage"], product["galleryThumbnails"], product["productOverview"]
        
        if product.get("aPlusContent", "eiei") != "eiei":
            del product["aPlusContent"]
        new_data.append(product)

    return new_data


def main():
    input_directory = "clean1"
    output_directory = "clean2"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            input_path = os.path.join(input_directory, filename)
            processed_data = process_variant_data(input_path)

            # Construct output filename
            base_name = os.path.splitext(filename)[
                0
            ]  # e.g., "assited_pull_up_machine_unique_clean"
            # Remove "_unique_clean" at the end if it exists
            base_name = re.sub(r"_unique_clean$", "", base_name)
            output_filename = base_name + "_clean2.json"
            output_path = os.path.join(output_directory, output_filename)

            with open(output_path, "w") as outfile:
                json.dump(processed_data, outfile, indent=4)

            print(f"Processed {input_path} -> {output_path}")


if __name__ == "__main__":
    main()
