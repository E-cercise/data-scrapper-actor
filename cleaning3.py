import os
import re
import json


def remove_keys(attributes, keys_to_remove):
    """
    Removes specified keys from a list of attribute dictionaries.
    
    :param attributes: List of dictionaries with 'key' and 'value'.
    :param keys_to_remove: List of keys to be removed.
    :return: List of dictionaries excluding specified keys.
    """
    return [attr for attr in attributes if attr["key"] not in keys_to_remove]



def value_of_attribute(attr_list, key: str):
    for att in attr_list:
        if att.get("key") == key:
            return att.get("value")
    return None


def process_data(json_file):
    
    new_data = []
    
    with open(json_file, "r") as file:
        data = json.load(file)

    for product in data:
        have_model_name = False
        have_material = False
        have_color = False
        have_weight = False
        
        model_name = None
        material = None
        color = None
        weight = None
    
    
        for y in product["attributes"]:
            
            if y["key"] == "Model Name":
                have_model_name = True
                model_name = y["value"]
            if y["key"] == "Material":
                have_material = True
                material = y["value"]
            if y["key"] == "Color":
                have_color = True
                color = y["value"]
            if y["key"] == "Item Weight":
                have_weight = True
                weight = y["value"]

        if not (have_model_name and have_material and have_color and have_weight):
            continue

        product["model_name"] = model_name
        product["color"] = color
        product["material"] = material
        product["weight"] = weight
        
        product["attributes"] = remove_keys(product["attributes"], ["Brand", "Model Name", "Material", "Color", "Item Weight", "ASIN", "Brand Name"])
        
        new_data.append(product)

    return new_data


def main():
    input_directory = "clean2"
    output_directory = "clean3"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            input_path = os.path.join(input_directory, filename)
            processed_data = process_data(input_path)

            # Construct output filename
            base_name = os.path.splitext(filename)[
                0
            ]  # e.g., "assited_pull_up_machine_unique_clean"
            # Remove "_unique_clean" at the end if it exists
            output_filename = base_name.replace("clean2", "clean") + ".json"
            
            output_path = os.path.join(output_directory, output_filename)

            with open(output_path, "w") as outfile:
                json.dump(processed_data, outfile, indent=4)

            print(f"Processed {input_path} -> {output_path}")


if __name__ == "__main__":
    main()
