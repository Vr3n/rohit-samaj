import json
import csv
import logging
import os

# Configure logging
log_file = "data_import.log"
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

try:
    # Load JSON file
    json_file = "sub_districs_state.json"

    if not os.path.exists(json_file):
        logging.error("JSON file not found: %s", json_file)
        raise FileNotFoundError(f"JSON file not found: {json_file}")

    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    records = data.get("records", [])
    if not records:
        logging.warning("No records found in JSON file.")
        raise ValueError("JSON file contains no records.")

    # Initialize sets to avoid duplicates
    states = set()
    districts = set()
    talukas = set()

    # Define CSV file paths
    csv_files = {
        "states": "states.csv",
        "districts": "districts.csv",
        "talukas": "talukas.csv",
    }

    # Open CSV files and write headers
    try:
        with open(csv_files["states"], "w", encoding="utf-8", newline="") as state_file, \
                open(csv_files["districts"], "w", encoding="utf-8", newline="") as district_file, \
                open(csv_files["talukas"], "w", encoding="utf-8", newline="") as taluka_file:

            state_writer = csv.writer(state_file)
            district_writer = csv.writer(district_file)
            taluka_writer = csv.writer(taluka_file)

            # Write headers
            state_writer.writerow(["id", "name", "country"])
            district_writer.writerow(["id", "name", "state"])
            taluka_writer.writerow(["id", "name", "district"])

            # Process JSON records
            for record in records:
                try:
                    state_id = record["state_code"]
                    state_name = record["state_name_english"].strip().replace(
                        "'", "''")

                    district_id = record["district_code"]
                    district_name = record["district_name_english"].strip().replace(
                        "'", "''")

                    taluka_id = record["subdistrict_code"]
                    taluka_name = record["subdistrict_name_english"].strip().replace(
                        "'", "''")

                    # Write state record
                    if state_id not in states:
                        states.add(state_id)
                        state_writer.writerow([state_id, state_name, 1])

                    # Write district record
                    if (district_id, state_id) not in districts:
                        districts.add((district_id, state_id))
                        district_writer.writerow(
                            [district_id, district_name, state_id])

                    # Write taluka record
                    if (taluka_id, district_id) not in talukas:
                        talukas.add((taluka_id, district_id))
                        taluka_writer.writerow(
                            [taluka_id, taluka_name, district_id])

                except KeyError as ke:
                    logging.error(f"Missing key in record: {ke}")
                except Exception as e:
                    logging.error(f"Error processing record {record}: {e}")

        logging.info("CSV files successfully generated: %s",
                     ", ".join(csv_files.values()))

    except IOError as io_error:
        logging.error("Error writing CSV files: %s", io_error)
        raise

except Exception as e:
    logging.critical("Fatal error in script: %s", e)
    raise
