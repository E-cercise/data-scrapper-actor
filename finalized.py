import os
import json

# Define paths
input_dir = "transformed"  # Directory containing JSON files
output_file = "equipments.json"  # Output file

category_mapping = {
    "assited_pull_up_machine.json": "assisted pull up machine",
    "barbells.json": "barbell",
    "battle_ropes.json": "battle rope",
    "bicep_curl_machine.json": "bicep curl machine",
    "cable_machine.json": "cable machine",
    "cable_machines.json": "cable machine",
    "calf_raise_machine.json": "calf raise machine",
    "chest_fly_machine.json": "chest fly machine",
    "chest_press_machine.json": "chess press machine",
    "dumbells.json": "dumbell",
    "elliptical.json": "elliptical",
    "kettlebells.json": "kettlebell",
    "lat_pulldown_machine.json": "lat pulldown machine",
    "leg_curl_machine.json": "leg curl machine",
    "leg_extension_machine.json": "leg extension machine",
    "leg_press_machine.json": "leg press machine",
    "medicine_balls.json": "medicine ball",
    "pec_deck_machine.json": "pec deck machine",
    "pull_up_bar.json": "pull up bar",
    "rowing_machine.json": "rowing machine",
    "seated_row_machine.json": "seated row machine",
    "shoulder_press_machine.json": "shoulder press machine",
    "stationary_bike.json": "stationary bike",
    "treadmill.json": "treadmill",
    "trx_suspension_trainer.json": "trx suspension trainer"
}

# Dictionary to store merged data
merged_data = {}

# Iterate over all JSON files in the directory
for filename in os.listdir(input_dir):
    if filename.endswith(".json"):  # Only process JSON files
        filepath = os.path.join(input_dir, filename)

        # Read the JSON file
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Process each entry
            for entry in data:
                asin = entry.get("asin")

                if asin:
                    if asin not in merged_data:
                        # Store the first occurrence of the entire entry
                        merged_data[asin] = entry
                        # Ensure muscle_group_used is a set for merging
                        merged_data[asin]["muscle_group_used"] = set(entry.get("muscle_group_used", []))
                        merged_data[asin]["category"] = category_mapping[filename]
                    else:
                        # Only merge muscle_group_used (keep other fields unchanged)
                        merged_data[asin]["muscle_group_used"].update(entry.get("muscle_group_used", []))

# Convert sets back to lists for JSON serialization
final_data = [
    {**item, "muscle_group_used": list(item["muscle_group_used"])}
    for item in merged_data.values()
]

# Write the merged data to the output JSON file
with open(output_file, "w", encoding="utf-8") as output:
    json.dump(final_data, output, indent=4, ensure_ascii=False)

print(f"✅ Merging complete! Data saved to {output_file}")
