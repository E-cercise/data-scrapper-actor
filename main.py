import json
import requests
import re
from io import BytesIO

# API Configuration
IMAGE_UPLOAD_URL = "http://127.0.0.1:8888/api/image/upload"
EQUIPMENT_ADD_URL = "http://127.0.0.1:8888/api/equipment"
BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mzg4NTAwNjMsIm5hbWUiOiJQcmVhd3BhbiBUaGFtYXBpcG9sIiwidXNlcl9pZCI6IjJkMmUzYWM1LTExYzctNDNiOS1iODUwLWQzNmU2M2M5ODU2NyJ9.kDrDrBtx0bsT5cHPfVWY7hO8BH-WJ6i6idEaXZopBAE"
EQUIPMENTS_JSON = "equipments.json"
LOG_FILE = "equipment_upload.log"

HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

def log_message(message):
    """Logs messages to a file and prints them to the console."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(message + "\n")
    print(message)

def extract_numeric_weight(weight_str):
    """Extracts the numeric value from a weight string like '51.8 Pounds'."""
    if isinstance(weight_str, (int, float)):
        return float(weight_str)  # Already a numeric value
    elif isinstance(weight_str, str):
        match = re.findall(r"[-+]?\d*\.\d+|\d+", weight_str)  # Extracts float or integer
        if match:
            return float(match[0])  # Convert first match to float
    return 0.0  # Default to 0.0 if extraction fails

def generate_placeholder_url(equipment_name, eq_option_name = ""):
    """Generates a placeholder image URL with the first 5 words of the equipment name."""
    words = equipment_name.split()[:5]  # Get first 5 words
    text_param = "+".join(words) + eq_option_name.replace(" ", "+")  # Replace spaces with +
    return f"https://placehold.co/600x400?text={text_param}/png"

def upload_image(image_url):
    """Synchronously uploads an image and returns Image ID."""
    log_message(f"⬆️ Uploading image: {image_url}")
    
    # Download the image
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code != 200:
            log_message(f"⚠️ Failed to download image: {image_url}")
            return None
        
        image_data = BytesIO(response.content)

        # Upload the image
        files = {"img": ("image.jpg", image_data, "image/jpeg")}
        upload_response = requests.post(IMAGE_UPLOAD_URL, files=files, headers={"Authorization": f"Bearer {BEARER_TOKEN}"})

        if upload_response.status_code == 200:
            image_id = upload_response.json().get("fileID")
            log_message(f"✅ Uploaded: {image_url} -> ImageID: {image_id}")
            return image_id
        else:
            log_message(f"❌ Image upload failed. Response: {upload_response.text()}")
            return None
    except Exception as e:
        log_message(f"❌ Error uploading image: {str(e)}")
        return None

def process_equipment_data():
    """Reads equipment data, uploads images, and sends formatted data synchronously."""
    try:
        with open(EQUIPMENTS_JSON, "r", encoding="utf-8") as file:
            equipments = json.load(file)

        for index, equipment in enumerate(equipments):
            equipment_name = equipment.get("title", "Unknown")
            log_message(f"\n--- Processing Equipment {index + 1}/{len(equipments)}: {equipment_name} ---")

            # Process images
            for option in equipment.get("equipment_options", []):
                if "img" in option:
                    for img in option["img"]:
                        if not img.get("link"):  # If link is null or missing, use a placeholder
                            img["link"] = generate_placeholder_url(equipment_name, option["name"])
                            log_message(f"🔹 Assigned placeholder image: {img['link']}")

                        # Upload the image
                        image_id = upload_image(img["link"])
                        if image_id:
                            img["id"] = image_id  # Replace URL with Image ID
                        del img["link"]  # Remove link field

            # Format Equipment JSON
            formatted_equipment = {
                "name": equipment.get("title", ""),
                "brand": equipment.get("brand", ""),
                "model": equipment.get("model_name", ""),
                "color": equipment.get("color", ""),
                "material": equipment.get("material", ""),
                "description": equipment.get("description", ""),
                "options": [
                    {
                        "name": option["name"],
                        "price": option["price"],
                        "weight": extract_numeric_weight(option["weight"]),
                        "available": option["remaining_products"],
                        "images": option.get("img", [])
                    }
                    for option in equipment.get("equipment_options", [])
                ],
                "muscle_group_used": equipment.get("muscle_group_used", []),
                "features": equipment.get("features", []),
                "additional_fields": [
                    {"key": attr["key"], "value": attr["value"]}
                    for attr in equipment.get("attributes", [])
                ]
            }

            # Send POST request to add equipment
            post_equipment(formatted_equipment)

    except Exception as e:
        log_message(f"❌ Error processing equipment data: {str(e)}")

def post_equipment(equipment_data):
    """Sends a synchronous POST request to add equipment with detailed error logging."""
    log_message(f"⬆️ Sending equipment data: {equipment_data['name']}")
    
    try:
        response = requests.post(EQUIPMENT_ADD_URL, json=equipment_data, headers=HEADERS)

        if response.status_code == 200:
            log_message(f"✅ Successfully added: {equipment_data['name']}")
        else:
            log_message(f"❌ Failed to add: {equipment_data['name']}. Status Code: {response.status_code}. Response: {response.text}")
            log_message(f"❗ Payload Sent: {json.dumps(equipment_data, indent=2)}")
    except Exception as e:
        log_message(f"❌ Error adding {equipment_data['name']}: {str(e)}")

if __name__ == "__main__":
    process_equipment_data()
