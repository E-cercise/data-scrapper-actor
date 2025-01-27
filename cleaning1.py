import os
import json

def remove_brand_from_attributes(attributes):
    """
    Removes any attribute dictionary where 'key' == 'Brand'.
    
    Args:
        attributes (list): List of attribute dictionaries.
    
    Returns:
        tuple: A tuple containing the cleaned attributes list and the number of removed attributes.
    """
    if not isinstance(attributes, list):
        return attributes, 0  # No changes if attributes is not a list
    
    original_length = len(attributes)
    cleaned_attributes = [attr for attr in attributes if attr.get("key") != "Brand"]
    removed_count = original_length - len(cleaned_attributes)
    
    return cleaned_attributes, removed_count

def process_json_file(input_filepath, output_filepath):
    """
    Processes a single JSON file to remove 'Brand' from attributes and save the cleaned data.
    
    Args:
        input_filepath (str): Path to the input JSON file.
        output_filepath (str): Path to save the cleaned JSON file.
    
    Returns:
        int: Number of 'Brand' attributes removed.
    """
    try:
        with open(input_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file {input_filepath}: {e}")
        return 0
    except Exception as e:
        print(f"Unexpected error reading file {input_filepath}: {e}")
        return 0
    
    if not isinstance(data, list):
        print(f"Skipping file {input_filepath}: Expected a list of records.")
        return 0
    
    total_removed = 0
    for record in data:
        attributes = record.get("attributes")
        if attributes:
            cleaned_attributes, removed = remove_brand_from_attributes(attributes)
            if removed > 0:
                record["attributes"] = cleaned_attributes
                total_removed += removed
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    
    # Save the cleaned data to the output file
    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error writing to file {output_filepath}: {e}")
        return total_removed  # Return the count even if saving fails
    
    return total_removed

def main():
    # Define the input and output directories
    INPUT_DIR = "clean"
    OUTPUT_DIR = "clean1"
    
    # Check if the input directory exists
    if not os.path.isdir(INPUT_DIR):
        print(f"The directory '{INPUT_DIR}' does not exist.")
        return
    
    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # List all JSON files ending with '_unique_clean.json' in the input directory
    json_files = [file for file in os.listdir(INPUT_DIR) if file.endswith("_unique_clean.json")]
    
    if not json_files:
        print(f"No JSON files ending with '_unique_clean.json' found in '{INPUT_DIR}'.")
        return
    
    print(f"Found {len(json_files)} JSON file(s) in '{INPUT_DIR}' to process.\n")
    
    # Dictionary to hold the number of removed attributes per file
    removal_summary = {}
    
    for json_file in json_files:
        input_filepath = os.path.join(INPUT_DIR, json_file)
        output_filepath = os.path.join(OUTPUT_DIR, json_file)
        
        removed_count = process_json_file(input_filepath, output_filepath)
        removal_summary[json_file] = removed_count
    
    # Display the summary
    print("=== Removal Summary ===\n")
    total_removed_all_files = 0
    for file, count in removal_summary.items():
        print(f"{file}: Removed {count} 'Brand' attribute(s).")
        total_removed_all_files += count
    print(f"\nTotal 'Brand' attributes removed across all files: {total_removed_all_files}")

if __name__ == "__main__":
    main()
