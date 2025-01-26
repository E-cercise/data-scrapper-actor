import os
import json

def process_files():
    # Define the folders
    input_folder = "data"
    output_folder = "clean0"

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all JSON files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, file_name.replace(".json", "_clean0.json"))

            group_product_options(input_file_path, output_file_path)

            # try:
            #     # Read the JSON data from the file
            #     with open(input_file_path, "r") as file:
            #         data = json.load(file)
                    

                # # Extract the required fields
                # cleaned_item = []
                # for index, item in enumerate(data):

                #     try:

                #         cleaned_item = {
                #             "asin": item.get("asin"),
                #             "title": item.get("title"),
                #             "price": item.get("price", {}).get("value"),
                #             "brand": item.get("brand"),
                #             "thumbnailImage": item.get("thumbnailImage"),
                #             "galleryThumbnails": item.get("galleryThumbnails"),
                #             "description": item.get("description"),
                #             "features": item.get("features"),
                #             "attributes": item.get("attributes"),
                #             "productOverview": item.get("productOverview"),
                #         }

                #         # Check for missing fields
                #         missing_fields = [
                #             field for field, value in cleaned_item.items() if value is None
                #         ]
                #         if missing_fields:
                #             print(
                #                 f"Warning: Missing fields {missing_fields} in item at index {index} in {file_name}"
                #             )

                #         cleaned_data.append(cleaned_item)
                #     except AttributeError as e:
                #         print(f"Error processing item at index {index} in {file_name}: {e}")
                #         raise

                # Write the cleaned data to the output file
            #     with open(output_file_path, "w") as output_file:
            #         json.dump(unique_items, output_file, indent=4)

            #     print(f"Processed: {file_name}")

            # except Exception as e:
            #     print(f"Error processing {file_name}: {e}")


def group_product_options(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    grouped_data = []

    for product in data:
        # Extract common attributes
        asin = product.get('asin')
        color = None
        size = None
        price = product.get('price', {}).get('value')

        # Extract attributes for product options
        attributes = product.get('attributes', [])
        for attr in attributes:
            if attr['key'].lower() == 'color':
                color = attr['value']
            elif attr['key'].lower() == 'size':
                size = attr['value']

        # Group product options
        product_option = {
            'color': color,
            'size': size,
            'price': price
        }

        # Remove attributes that are grouped into product_option
        product.pop('attributes', None)
        product.pop('price', None)

        # Check if this ASIN already exists in grouped_data
        existing_product = next((p for p in grouped_data if p['asin'] == asin), None)
        if existing_product:
            existing_product['product_option'].append(product_option)
        else:
            # Add new product entry           product['product_option'] = [product_option]
            grouped_data.append(product)

    # Save the grouped data to the output file
    with open(output_file, 'w') as file:
        json.dump(grouped_data, file, indent=4)

    print(f"Grouped data saved to {output_file}")

if __name__ == "__main__":
    process_files()
