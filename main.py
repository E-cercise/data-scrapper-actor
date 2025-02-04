import aiohttp
import asyncio
import json
from io import BytesIO

# API Configuration
IMAGE_UPLOAD_URL = "http://127.0.0.1:8888/api/image/upload"
EQUIPMENT_ADD_URL = "http://127.0.0.1:8888/api/equipment"
BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mzg2NzQ3OTEsIm5hbWUiOiJQcmVhd3BhbiBUaGFtYXBpcG9sIiwidXNlcl9pZCI6IjQyYTUzYTkzLWU0NDUtNDRhMy1iZjEzLWZkNjc4NTUwM2Y0NCJ9.B2o9imViq6ogziR36GIcLDHNtmcPdFTv9SyLWVvOuZs"
EQUIPMENTS_JSON = "equipments.json"
LOG_FILE = "equipment_upload.log"

HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

async def log_message(message):
    """Logs messages to a file and prints them to the console."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(message + "\n")
    print(message)

async def upload_image(session, image_url):
    """Downloads an image from a URL and uploads it asynchronously."""
    try:
        async with session.get(image_url) as response:
            if response.status == 200:
                image_data = await response.read()  # Get binary content
                
                # Correctly format multipart/form-data
                form_data = aiohttp.FormData()
                form_data.add_field("img", 
                                    BytesIO(image_data),
                                    filename="image.jpg",
                                    content_type="image/jpeg")

                async with session.post(IMAGE_UPLOAD_URL, data=form_data, headers=HEADERS) as upload_response:
                    if upload_response.status == 200:
                        result = await upload_response.json()
                        image_id = result.get("fileID")
                        await log_message(f"✅ Uploaded {image_url} -> ImageID: {image_id}")
                        return image_id
                    else:
                        await log_message(f"⚠️ Failed to upload {image_url}. Response: {await upload_response.text()}")
            else:
                await log_message(f"⚠️ Failed to download {image_url}. Status Code: {response.status}")
    except Exception as e:
        await log_message(f"❌ Error uploading {image_url}: {str(e)}")
    return None

async def process_equipment_data():
    """Reads equipment data, uploads images, and sends formatted data asynchronously."""
    try:
        with open(EQUIPMENTS_JSON, "r", encoding="utf-8") as file:
            equipments = json.load(file)

        async with aiohttp.ClientSession() as session:
            tasks = []
            for index, equipment in enumerate(equipments):
                await log_message(f"\n--- Processing Equipment {index + 1}/{len(equipments)}: {equipment['title']} ---")

                # Process images concurrently
                image_tasks = []
                for option in equipment.get("equipment_options", []):
                    if "img" in option:
                        for img in option["img"]:
                            if "link" in img:
                                image_tasks.append(upload_image(session, img["link"]))

                # Wait for all images to be uploaded
                uploaded_image_ids = await asyncio.gather(*image_tasks)

                # Replace image URLs with their corresponding IDs
                img_idx = 0
                for option in equipment.get("equipment_options", []):
                    for img in option["img"]:
                        if "link" in img:
                            if uploaded_image_ids[img_idx]:
                                img["id"] = uploaded_image_ids[img_idx]  # Replace URL with Image ID
                            del img["link"]  # Remove link field
                            img_idx += 1

                # Format Equipment JSON
                formatted_equipment = {
                    "name": equipment["title"],
                    "brand": equipment["brand"],
                    "model": equipment["model_name"],
                    "color": equipment["color"],
                    "material": equipment["material"],
                    "description": equipment.get("description", ""),
                    "option": [
                        {
                            "name": option["name"],
                            "price": option["price"],
                            "weight": option["weight"],
                            "available": option["remaining_products"],
                            "images": option.get("img", [])  # List of Image IDs
                        }
                        for option in equipment.get("equipment_options", [])
                    ],
                    "muscle_group_used": equipment.get("muscle_group_used", []),
                    "feature": equipment.get("features", []),
                    "additional_field": [
                        {"key": attr["key"], "value": attr["value"]}
                        for attr in equipment.get("attributes", [])
                    ]
                }

                # Send POST request to add equipment (async)
                tasks.append(post_equipment(session, formatted_equipment))

            # Wait for all equipment records to be added concurrently
            await asyncio.gather(*tasks)

    except Exception as e:
        await log_message(f"❌ Error processing equipment data: {str(e)}")

async def post_equipment(session, equipment_data):
    """Sends an async POST request to add equipment."""
    try:
        async with session.post(EQUIPMENT_ADD_URL, json=equipment_data, headers=HEADERS) as response:
            if response.status == 200:
                await log_message(f"✅ Successfully added: {equipment_data['name']}")
            else:
                await log_message(f"❌ Failed to add: {equipment_data['name']}. Response: {await response.text()}")
    except Exception as e:
        await log_message(f"❌ Error adding {equipment_data['name']}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(process_equipment_data())
