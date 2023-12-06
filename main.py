import streamlit as st
from st_draggable_list import DraggableList
import pandas as pd

def initialize_session_state(default_values) -> None:
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

def load_css() -> list:
    pass

def change_page() -> None:
    pass

def compile_dictionary_for_generator() -> dict:
    # Retrieve values from the custom input option, save in a list for labels and formatting respectively ---
    labels = [st.session_state.labels[i] for i in range(5)]
    format = [st.session_state.format[i] for i in range(5)]

    # Generate a dictionary with label als formatting as key, value pairs
    items = dict(zip(labels, format))

    # List comprehension to get selected items with their order - list of dictionaries
    selected_items = [{'name': key, 'order': order} for order, (key, selected) in enumerate(st.session_state.selection.items()) if selected]

    # Combine the dictionaries into one - selected_items is unpacked and placed first in the new dictionary
    return {**{item['name']: item['order'] for item in selected_items}, **items}

def compile_draggablelist() -> dict:

    # call dictionary generator to retrieve necessary values
    combined_dict = compile_dictionary_for_generator()

    # Use listcomprehension to generate a new list of dictionaries, for each item in original - keeping only the order and key values. 
    return [{'name': key, 'order': order} for order, (key, item) in enumerate(combined_dict.items()) if item != "" and key != ""]

def compile_list_for_dataframe() -> dict:
    pass

def generate_data():
    pass

def download_data() -> None:
    pass


# --- Set default variables ---
default_values = {
    'css': [],
    'selection': {},
    'labels': {},
    'format': {},
    'selectionitems': ['Name', 'Surname', 'Street Address', 'Zipcode', 'Phonenumber', 'Occupation', 'Hobby'],
}



# --- Initialize session with default values ---
initialize_session_state(default_values)

# --- custimize page with css file ---
with open("selection.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Selection page ---
# generate columenview of easiere navigation
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('### **Select fields**')
    for item in st.session_state.selectionitems:
        st.session_state.selection[item] = st.toggle(item)

with col2:
    st.markdown('### **Column label**')
    for i in range(5):
        st.session_state.labels[i] = st.text_input(
            label=f"{i}", placeholder=f'label {i+1}', key=f'label_input_{i}'
        )

with col3:
    st.markdown('### **Format**')
    for i in range(5):
        st.session_state.format[i] = st.text_input(
            label=f"{i}", placeholder='Input format', key=f'input_{i}'
        )


# --- Order of items page ---

slist = DraggableList(compile_draggablelist())


# --- Dataframe preview and download ---
# Check if selected_items is not None
# if selected_items:
#     # Create a DataFrame with selected items as columns
#     column_names = [item.key for item in selected_items]
#     df = pd.DataFrame(columns=column_names, index=None)

#     # Display the DataFrame
#     st.dataframe(df.head(), hide_index=True, use_container_width=True)