import json
import random

# Load the content of a JSON file
def load_json(filename):
    """Reads and returns the content of a JSON file."""
    with open(filename, 'r') as file:
        return json.load(file)

# Save the combined and shuffled content to a new JSON file
def save_json(filename, data):
    """Saves the given data to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Combine and shuffle two JSON files
def combine_and_randomize(file1, file2, output_file):
    """Combines two JSON files and saves the randomized result in a new file."""
    # Load the content of both files
    data1 = load_json(file1)
    data2 = load_json(file2).get("feedback_data")

    # Combine both lists (assuming the root of each JSON is a list)
    combined_data = data1 + data2

    # Shuffle the combined list
    random.shuffle(combined_data)

    # Save the shuffled result to the output file
    save_json(output_file, combined_data)

# Main logic to combine and randomize the two files
if __name__ == "__main__":
    # Input JSON file names
    file1 = "CRM_feedback.json"
    file2 = "feedback_mockdata.json"

    # Output JSON file name
    output_file = "combined_feedback.json"

    # Call the function to combine and randomize the JSON files
    combine_and_randomize(file1, file2, output_file)
