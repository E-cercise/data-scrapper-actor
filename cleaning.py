import os
import json

def process_files():
    # Define the folders
    input_folder = "remove_duplicate_asin_data"
    output_folder = "clean"

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all JSON files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, file_name.replace(".json", "_clean.json"))

        # try:
            # Read the JSON data from the file
            with open(input_file_path, "r") as file:
                data = json.load(file)
                

            # Extract the required fields
            cleaned_data = []
            for index, item in enumerate(data):

                try:
                    price = item.get("price", {})
                    
                    if price is not None:
                        price = price.get("value")

                    cleaned_item = {
                        "asin": item.get("asin"),
                        "title": item.get("title"),
                        "price": price,
                        "brand": item.get("brand"),
                        "thumbnailImage": item.get("thumbnailImage"),
                        "galleryThumbnails": item.get("galleryThumbnails"),
                        "description": item.get("description", ""),
                        "features": item.get("features"),
                        "attributes": item.get("attributes"),
                        "productOverview": item.get("productOverview"),
                        "variantDetails": item.get("variantDetails"),
                        "variantAttributes": item.get("variantAttributes")
                    }

                    # Check for missing fields
                    missing_fields = [
                        field for field, value in cleaned_item.items() if value is None
                    ]
                    if missing_fields:
                        print(
                            f"Warning: Missing fields {missing_fields} in item at index {index} in {file_name}"
                        )

                    cleaned_data.append(cleaned_item)
                except AttributeError as e:
                    print(f"{item}")
                    print()
                    print()
                    print(type(item[index]))
                    print(f"Error processing item at index {index} in {file_name}: {e}")
                    raise

            # Write the cleaned data to the output file
            with open(output_file_path, "w") as output_file:
                json.dump(cleaned_data, output_file, indent=4)

            print(f"Processed: {file_name}")

        # except Exception as e:
        #     print(f"Error processing {file_name}: {e}")


if __name__ == "__main__":
    process_files()
    