import os
import json

muscle_mapper = {
    "clean3/chest_press_machine_clean.json": [
        "ft_7",
        "ft_8",
        "ft_14",
        "ft_15",
        "ft_5",
        "ft_6",
    ],
    "clean3/assited_pull_up_machine_clean.json": [
        "bk_1",
        "bk_6",
        "bk_7",
        "bk_2",
        "bk_3",
    ],
    "clean3/calf_raise_machine_clean.json": ["bk_30", "bk_31", "ft_38", "ft_39"],
    "clean3/stationary_bike_clean.json": [
        "ft_38",
        "ft_39",
        "bk_22",
        "bk_23",
        "ft_26",
        "ft_27",
    ],
    "clean3/leg_extension_machine_clean.json": ["ft_26", "ft_27"],
    "clean3/seated_row_machine_clean.json": ["bk_6", "bk_7", "bk_10", "bk_11"],
    "clean3/leg_curl_machine_clean.json": [
        "bk_22",
        "bk_23",
        "bk_24",
        "bk_25",
        "bk_26",
        "bk_27",
        "bk_30",
        "bk_31",
    ],
    "clean3/cable_machines_clean.json": ["bk_10", "bk_11", "bk_12", "bk_13"],
    "clean3/pec_deck_machine_clean.json": ["ft_7", "ft_8", "ft_10", "ft_11"],
    "clean3/rowing_machine_clean.json": [
        "bk_1",
        "bk_6",
        "bk_7",
        "bk_10",
        "bk_11",
        "ft_14",
        "ft_15",
        "ft_9",
    ],
    "clean3/barbells_clean.json": [
        "ft_7",
        "ft_8",
        "bk_1",
        "bk_6",
        "bk_7",
        "bk_2",
        "bk_3",
        "bk_8",
        "bk_9",
        "ft_5",
        "ft_6",
        "ft_14",
        "ft_15",
        "bk_10",
        "bk_11",
        "ft_16",
        "ft_17",
        "ft_20",
        "ft_21",
        "bk_20",
        "bk_21",
        "ft_24",
        "ft_25",
        "bk_28",
        "bk_29",
        "ft_32",
        "ft_33",
        "bk_22",
        "bk_23",
        "bk_24",
        "bk_25",
        "bk_26",
        "bk_27",
        "bk_30",
        "bk_31",
        "ft_38",
        "ft_39",
        "ft_9",
        "ft_12",
        "ft_13",
        "bk_16",
        "bk_17",
        "bk_18",
        "bk_19",
    ],
    "clean3/battle_ropes_clean.json": [
        "ft_5",
        "ft_6",
        "bk_10",
        "bk_11",
        "ft_14",
        "ft_15",
        "ft_9",
    ],
    "clean3/medicine_balls_clean.json": [
        "ft_9",
        "ft_7",
        "ft_8",
        "ft_14",
        "ft_15",
        "ft_16",
        "ft_17",
    ],
    "clean3/shoulder_press_machine_clean.json": [
        "bk_8",
        "bk_9",
        "bk_5",
        "bk_6",
        "bk_1",
        "ft_3",
        "ft_4",
    ],
    "clean3/chest_fly_machine_clean.json": ["ft_7", "ft_8", "ft_10", "ft_11"],
    "clean3/bicep_curl_machine_clean.json": ["ft_14", "ft_15", "ft_16", "ft_17"],
    "clean3/kettlebells_clean.json": [
        "bk_8",
        "bk_9",
        "ft_5",
        "ft_6",
        "bk_1",
        "bk_6",
        "bk_7",
        "bk_2",
        "bk_3",
        "ft_14",
        "ft_15",
        "bk_10",
        "bk_11",
        "ft_16",
        "ft_17",
        "ft_20",
        "ft_21",
        "bk_20",
        "bk_21",
        "ft_24",
        "ft_25",
        "bk_28",
        "bk_29",
        "ft_32",
        "ft_33",
        "bk_22",
        "bk_23",
        "bk_24",
        "bk_25",
        "bk_26",
        "bk_27",
        "bk_30",
        "bk_31",
        "ft_38",
        "ft_39",
        "ft_9",
        "ft_12",
        "ft_13",
        "bk_16",
        "bk_17",
        "bk_18",
        "bk_19",
    ],
    "clean3/dumbells_clean.json": [
        "ft_7",
        "ft_8",
        "bk_1",
        "bk_6",
        "bk_7",
        "bk_8",
        "bk_9",
        "ft_5",
        "ft_6",
        "ft_14",
        "ft_15",
        "bk_10",
        "bk_11",
        "ft_16",
        "ft_17",
        "ft_20",
        "ft_21",
        "bk_20",
        "bk_21",
        "ft_24",
        "ft_25",
        "bk_22",
        "bk_23",
        "bk_30",
        "bk_31",
        "ft_38",
        "ft_39",
        "ft_9",
        "ft_12",
        "ft_13",
    ],
    "clean3/elliptical_clean.json": [
        "ft_38",
        "ft_39",
        "ft_26",
        "ft_27",
        "bk_22",
        "bk_23",
    ],
    "clean3/lat_pulldown_machine_clean.json": [
        "bk_1",
        "bk_2",
        "bk_3",
        "bk_4",
        "bk_5",
        "bk_6",
    ],
    "clean3/pull_up_bar_clean.json": ["bk_1", "bk_6", "bk_7", "bk_2", "bk_3"],
    "clean3/trx_suspension_trainer_clean.json": [
        "ft_7",
        "ft_8",
        "bk_1",
        "bk_6",
        "bk_7",
        "bk_2",
        "bk_3",
        "bk_8",
        "bk_9",
        "ft_5",
        "ft_6",
        "ft_3",
        "ft_4",
        "ft_14",
        "ft_15",
        "bk_10",
        "bk_11",
        "ft_16",
        "ft_17",
        "ft_20",
        "ft_21",
        "bk_20",
        "bk_21",
        "ft_24",
        "ft_25",
        "bk_28",
        "bk_29",
        "ft_32",
        "ft_33",
        "bk_22",
        "bk_23",
        "bk_24",
        "bk_25",
        "bk_26",
        "bk_27",
        "bk_30",
        "bk_31",
        "ft_38",
        "ft_39",
        "ft_26",
        "ft_27",
        "ft_9",
        "ft_12",
        "ft_13",
        "bk_16",
        "bk_17",
        "bk_18",
        "bk_19",
    ],
    "clean3/leg_press_machine_clean.json": [
        "bk_20",
        "bk_21",
        "bk_24",
        "bk_25",
        "bk_22",
        "bk_23",
        "bk_28",
        "bk_29",
        "ft_32",
        "ft_33",
    ],
    "clean3/treadmill_clean.json": [
        "bk_30",
        "bk_31",
        "ft_38",
        "ft_39",
        "bk_22",
        "bk_23",
        "ft_26",
        "ft_27",
    ],
    "clean3/cable_machine_clean.json": [
        "ft_7",
        "ft_8",
        "bk_1",
        "bk_6",
        "bk_7",
        "bk_2",
        "bk_3",
        "bk_8",
        "bk_9",
        "ft_5",
        "ft_6",
        "ft_3",
        "ft_4",
        "ft_14",
        "ft_15",
        "bk_10",
        "bk_11",
        "ft_16",
        "ft_17",
        "ft_20",
        "ft_21",
        "bk_20",
        "bk_21",
        "ft_24",
        "ft_25",
        "bk_28",
        "bk_29",
        "ft_32",
        "ft_33",
        "bk_22",
        "bk_23",
        "bk_24",
        "bk_25",
        "bk_26",
        "bk_27",
        "bk_30",
        "bk_31",
        "ft_38",
        "ft_39",
        "ft_26",
        "ft_27",
        "ft_9",
        "ft_12",
        "ft_13",
        "bk_16",
        "bk_17",
        "bk_18",
        "bk_19",
    ],
}


def process_data(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    for product in data:
        product["muscle_group_used"] = muscle_mapper[json_file]

    return data


def main():
    input_directory = "clean3"
    output_directory = "transformed"

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
            output_filename = base_name.replace("_clean", "") + ".json"

            output_path = os.path.join(output_directory, output_filename)

            with open(output_path, "w") as outfile:
                json.dump(processed_data, outfile, indent=4)

            print(f"Processed {input_path} -> {output_path}")


if __name__ == "__main__":
    main()
