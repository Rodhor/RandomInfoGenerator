from faker import Faker
import pandas as pd
import random

# Create a Faker object with the German locale
fake = Faker(["DE_de"])


# Function to generate synthetic data based on a selection dictionary
def generate_data(selection_data_dict, number_of_entries) -> dict:
    # Extract 'name' entries from the selection data and convert to lowercase with underscores
    selection_items = [
        item["name"].lower().replace(" ", "_")
        for item in selection_data_dict
        if "name" in item
    ]
    # Generate synthetic data using Faker for each selected item
    generated_data = {
        item: [getattr(fake, item)() for _ in range(number_of_entries)]
        for item in selection_items
    }
    return generated_data


# Function to generate custom synthetic data based on a custom data dictionary
def generate_custom_data(custom_data_dict, number_of_entries) -> dict:
    # Iterate through the custom data dictionary
    for key, value in custom_data_dict.items():
        generated_entries = []
        # Generate synthetic data for each custom item
        for _ in range(number_of_entries):
            generated_value = ""
            # Replace '?' with a random uppercase letter and '#' with a random digit
            for char in value:
                if char == "?":
                    generated_value += fake.random_letter().upper()
                elif char == "#":
                    generated_value += str(random.randint(0, 9))
                else:
                    generated_value += char
            generated_entries.append(generated_value)
        custom_data_dict[key] = generated_entries

    return custom_data_dict


# Function to generate a DataFrame with synthetic data
def generate_dataframe(
    column_names_list, custom_data_dict, selection_data, number_of_entries
) -> pd.DataFrame:
    try:
        # Extract 'name' entries from the column_names_list and convert to lowercase with underscores
        column_names = [
            dictionary["name"].lower().replace(" ", "_")
            for dictionary in column_names_list
        ]
        # Generate synthetic data for both selection and custom data
        selection = generate_data(selection_data, number_of_entries)
        custom = generate_custom_data(custom_data_dict, number_of_entries)
        # Combine selection and custom data into a single dictionary
        data = {**selection, **custom}
        # Create a DataFrame using column names and synthetic data
        df = pd.DataFrame(columns=column_names, data=data)

    # Handle exceptions related to user input errors, page reloads to prevent recurrence
    except:
        pass

    return df
