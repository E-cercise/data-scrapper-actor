import json
import random

# File paths
INPUT_FILE = "equipments.json"       # Full dataset
OUTPUT_FILE = "sample_equipments.json"  # Output sample file

# Number of samples to extract
NUM_SAMPLES = random.randint(5, 10)  # Pick a random number between 5 and 10

def create_sample_file():
    """Reads equipment data, extracts a sample, and writes it to a new file."""
    try:
        # Read full equipment data
        with open(INPUT_FILE, "r", encoding="utf-8") as file:
            equipments = json.load(file)

        # Ensure we don't sample more than the available data
        sample_size = min(NUM_SAMPLES, len(equipments))

        # Randomly select sample records
        sample_records = random.sample(equipments, sample_size)

        # Write samples to a new file
        with open(OUTPUT_FILE, "w", encoding="utf-8") as sample_file:
            json.dump(sample_records, sample_file, indent=2)

        print(f"✅ Successfully created {OUTPUT_FILE} with {sample_size} records.")

    except Exception as e:
        print(f"❌ Error creating sample file: {str(e)}")

# Run the function
if __name__ == "__main__":
    create_sample_file()
