import json
import asyncio
import aiohttp
from io import BytesIO

# API Configuration
IMAGE_UPLOAD_URL = "http://127.0.0.1:8888/api/image/upload"
EQUIPMENT_ADD_URL = "http://127.0.0.1:8888/api/equipment"
BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mzg2OTM4ODAsIm5hbWUiOiJQcmVhd3BhbiBUaGFtYXBpcG9sIiwidXNlcl9pZCI6ImI0MzIxMDc2LTViNTAtNGNmNy1hNTE2LTI2OWMwZDdjOGYwZCJ9.5lAZa0po1Uek9CHOGB57FZYPaJcWfoUno7ZZH41CkyI"
EQUIPMENTS_JSON = "equipments.json"
LOG_FILE = "equipment_upload.log"

HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

# Limit concurrent image uploads to prevent timeouts
SEM = asyncio.Semaphore(4)  # Max 4 concurrent uploads

async def log_message(message):
    """Logs messages to a file and prints them to the console."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(message + "\n")
    print(message)

# --- Async Image Upload with Retry ---
async def upload_image(session, image_url, retries=3, delay=5):
    """Downloads an image from a URL and uploads it asynchronously with retry."""
    async with SEM:  # Limit concurrent uploads
        for attempt in range(retries):
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

                        async with session.post(IMAGE_UPLOAD_URL, data=form_data, headers={"Authorization": f"Bearer {BEARER_TOKEN}"}) as upload_response:
                            if upload_response.status == 200:
                                result = await upload_response.json()
                                image_id = result.get("fileID")
                                await log_message(f"✅ Uploaded {image_url} -> ImageID: {image_id}")
                                return image_id
                            else:
                                await log_message(f"⚠️ Failed to upload {image_url}. Response: {await upload_response.text()}")

                # If request failed, retry after a short delay
                await log_message(f"🔄 Retrying {image_url} (Attempt {attempt + 1}/{retries})...")
                await asyncio.sleep(delay)

            except Exception as e:
                await log_message(f"❌ Error uploading {image_url} (Attempt {attempt + 1}/{retries}): {str(e)}")

    await log_message(f"❌ Final failure: Could not upload {image_url} after {retries} attempts.")
    return None

# --- Async Equipment Processing ---
async def process_equipment_data():
    """Reads equipment data, uploads images, and sends formatted data asynchronously."""
    try:
        with open(EQUIPMENTS_JSON, "r", encoding="utf-8") as file:
            equipments = json.load(file)

        async with aiohttp.ClientSession() as session:
            tasks = []
            for index, equipment in enumerate(equipments):
                await log_message(f"\n--- Processing Equipment {index + 1}/{len(equipments)}: {equipment.get('title', 'Unknown')} ---")

                # Process images concurrently
                image_tasks = []
                for option in equipment.get("equipment_options", []):
                    if "img" in option:
                        for img in option["img"]:
                            if "link" in img:
                                if not img["link"]:
                                    opt_name_abb = option["name"].replace(" ", "+")
                                    img["link"] = f"https://placehold.co/600x400?text={opt_name_abb}"
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
                    "name": equipment.get("title", ""),
                    "brand": equipment.get("brand", ""),
                    "model": equipment.get("model_name", ""),
                    "color": equipment.get("color", ""),
                    "material": equipment.get("material", ""),
                    "description": equipment.get("description", "") or "",
                    "options": [
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
                    "features": equipment.get("features", []),
                    "additional_fields": [
                        {"key": attr["key"], "value": attr["value"]}
                        for attr in equipment.get("attributes", [])
                    ]
                }

                # Send POST request to add equipment (async)
                tasks.append(post_equipment(session, formatted_equipment))

            # FIX: Wait for all async requests (Prevents "coroutine not awaited" issue)
            await asyncio.gather(*tasks)

    except Exception as e:
        await log_message(f"❌ Error processing equipment data: {str(e)}")

# --- Async API Call to Add Equipment ---
async def post_equipment(session, equipment_data):
    """Sends an async POST request to add equipment with detailed error logging."""
    try:
        async with session.post(EQUIPMENT_ADD_URL, json=equipment_data, headers=HEADERS) as response:
            response_text = await response.text()
            if response.status == 200:
                await log_message(f"✅ Successfully added: {equipment_data['name']}")
            else:
                await log_message(f"❌ Failed to add: {equipment_data['name']}. Status Code: {response.status}. Response: {response_text}")
                await log_message(f"❗ Payload Sent: {json.dumps(equipment_data, indent=2)}")  # Log JSON payload
    except Exception as e:
        await log_message(f"❌ Error adding {equipment_data['name']}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(process_equipment_data())
