import streamlit as st
from st_draggable_list import DraggableList
import pandas as pd
from generator import generate_dataframe


def initialize_session_state(default_values) -> None:
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_css() -> list:
    pass


def change_page() -> None:
    pass


def customdata_dict() -> dict:
    # Retrieve values from the custom input option, save in a list for labels and formatting respectively ---
    labels = [st.session_state.labels[i] for i in range(5)]
    format = [st.session_state.format[i] for i in range(5)]

    # Generate a dictionary with label als formatting as key, value pairs
    return dict(zip(labels, format))


def selectiondata_dict() -> dict:
    # List comprehension to get selected items with their order - list of dictionaries
    return [{'name': key, 'order': order} for order, (key, selected) in enumerate(
        st.session_state.selection.items()) if selected]


def compile_dictionary(custom_items, selection_items) -> dict:

    # Combine the dictionaries into one - selected_items is unpacked and placed first in the new dictionary
    return {**{item['name']: item['order'] for item in selection_items}, **custom_items}


def compile_draggablelist() -> dict:

    selection_items = selectiondata_dict()
    custom_items = customdata_dict()

    # call dictionary generator to retrieve necessary values
    combined_dict = compile_dictionary(custom_items, selection_items)

    # Use listcomprehension to generate a new list of dictionaries, for each item in original - keeping only the order and key values.
    return [{'name': key, 'order': order} for order, (key, item) in enumerate(combined_dict.items()) if item != "" and key != ""]


def generate_data_in_dataframe(column_names_list) -> pd.DataFrame:
    custom_data = customdata_dict()
    selection_data = selectiondata_dict()
    return generate_dataframe(column_names_list, custom_data, selection_data)


def download_data() -> None:
    pass


# --- Set default variables ---
default_values = {
    'css': [],
    'selection': {},
    'labels': {},
    'format': {},
    'selectionitems': ['First Name', 'Last name', 'Date of birth', 'Country', 'Address', 'City', 'Postcode', 'Current Country', 'Phone number', 'Job']
}

# --- Initialize session with default values ---
initialize_session_state(default_values)

# --- custimize page with css file ---
with open("selection.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Selection page ---
# generate columenview of ease of navigation
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
if st.button('ok'):
    st.dataframe(generate_data_in_dataframe(slist), hide_index=True)
