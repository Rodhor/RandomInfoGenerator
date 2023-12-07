from faker import Faker
import pandas as pd
import random

fake = Faker(['DE_de'])


def generate_data(selection_data_dict, number_of_entries=10) -> list:

    selection_items = [item['name'].lower().replace(' ', '_')
                       for item in selection_data_dict if 'name' in item]
    generated_data = {item: [getattr(fake, item)()
                             for _ in range(number_of_entries)] for item in selection_items}
    return generated_data


def generate_custom_data(custom_data_dict, number_of_entries=10) -> dict:
    for key, value in custom_data_dict.items():
        generated_entries = []
        for _ in range(number_of_entries):
            generated_value = ""
            for char in value:
                if char == '?':
                    generated_value += fake.random_letter().upper()
                elif char == '#':
                    generated_value += str(random.randint(0, 9))
                else:
                    generated_value += char

            generated_entries.append(generated_value)

        custom_data_dict[key] = generated_entries

    return custom_data_dict


def generate_dataframe(column_names_list, custom_data_dict, selection_data) -> pd.DataFrame:
    # List comprehension to retrieve keys from each dictionary
    try:
        column_names = [dictionary['name'].lower().replace(' ', '_')
                        for dictionary in column_names_list]
        selection = generate_data(selection_data)
        custom = generate_custom_data(custom_data_dict)
        data = {**selection, **custom}

        df = pd.DataFrame(columns=column_names, data=data).head()

    # Handel exeption of user inputerror. Page will reload and error will not occur again - therefor just pass
    except:
        pass

    return df
