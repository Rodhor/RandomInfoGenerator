# Import necessary libraries
import streamlit as st
from st_draggable_list import DraggableList
import pandas as pd
from generator import generate_dataframe  # Assuming a custom generator module
import io


# Function to initialize session state with default values
def initialize_session_state(default_values) -> None:
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value
    load_css()


# Function to load CSS styles
def load_css() -> None:
    # Define CSS files for different pages
    css_files = {"input": "input.css", "order": "order.css", "preview": "preview.css"}

    for key, file_path in css_files.items():
        with open(file_path, "r") as file:
            content = file.read()
            st.session_state.css[key] = content


# Function to change the current page
def change_page(page) -> None:
    st.session_state.page = page


# Function to set page style using loaded CSS
def set_page():
    st.markdown(
        f"<style>{st.session_state.css[st.session_state.page]}</style>",
        unsafe_allow_html=True,
    )


# Function to create a dictionary based on user inputs for custom data
def customdata_dict() -> dict:
    # Retrieve user input for column labels and formats
    labels = [st.session_state.labels[i] for i in range(7)]
    format = [st.session_state.format[i] for i in range(7)]
    return dict(zip(labels, format))


# Function to create a list of dictionaries based on user selections for selection data
def selectiondata_dict() -> dict:
    return [
        {"name": key, "order": order}
        for order, (key, selected) in enumerate(st.session_state.selection.items())
        if selected
    ]


# Function to compile dictionaries into one based on user selections
def compile_dictionary(custom_items, selection_items) -> dict:
    return {**{item["name"]: item["order"] for item in selection_items}, **custom_items}


# Function to compile a draggable list based on user selections and custom data
def compile_draggablelist() -> dict:
    selection_items = selectiondata_dict()
    custom_items = customdata_dict()
    combined_dict = compile_dictionary(custom_items, selection_items)
    return [
        {"name": key, "order": order}
        for order, (key, item) in enumerate(combined_dict.items())
        if item != "" and key != ""
    ]


# Function to generate a DataFrame with synthetic data based on user inputs
def generate_data_in_dataframe(column_names_list) -> pd.DataFrame:
    custom_data = customdata_dict()
    selection_data = selectiondata_dict()
    return generate_dataframe(column_names_list, custom_data, selection_data, entries)


# Function to generate BytesIO objects for CSV, Excel, and Pickle files
def generate_download_files(df):
    # CSV
    csv_file = io.BytesIO()
    df.to_csv(csv_file, index=False)
    csv_file.seek(0)

    # Excel
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine="openpyxl") as excel_writer:
        df.to_excel(excel_writer, index=False, sheet_name="Sheet1")
    excel_file.seek(0)

    # Pickle
    pickle_file = io.BytesIO()
    df.to_pickle(pickle_file)
    pickle_file.seek(0)

    return csv_file, excel_file, pickle_file


# Set default values for the session state
default_values = {
    "css": {},
    "page": "input",
    "selection": {},
    "labels": {},
    "format": {},
    "selectionitems": [
        "First Name",
        "Last name",
        "Date of birth",
        "Country",
        "Address",
        "City",
        "Postcode",
        "Current Country",
        "Phone number",
        "Job",
    ],
    "dataset": "",
}

# Initialize session with default values
initialize_session_state(default_values)

# Set the CSS style for the current page
set_page()

# Selection page
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### **Select fields**")
        for item in st.session_state.selectionitems:
            st.session_state.selection[item] = st.toggle(item)

    with col2:
        st.markdown("### **Column label**")
        for i in range(7):
            st.session_state.labels[i] = st.text_input(
                label=f"{i}", placeholder=f"label {i+1}", key=f"label_{i}"
            )

    with col3:
        st.markdown("### **Format**")
        for i in range(7):
            st.session_state.format[i] = st.text_input(
                label=f"{i}",
                placeholder="Input format",
                key=f"format_{i}",
                help=f"Specify the format for element {i}. Use '#' to represent random numbers and '?' to represent random letters. For example, '###???x' might generate '123ABCx'.",
            )

    entries = st.number_input(
        "Number of rows", min_value=1000, max_value=100_000, step=1000
    )

    selections_made = any(st.session_state.selection.values())
    inputs_provided = any(st.session_state.labels.values()) and any(
        st.session_state.format.values()
    )

    button_disabled = not (selections_made or inputs_provided)

    st.button(
        "Order",
        key="input_to_order",
        on_click=lambda: change_page("order"),
        disabled=button_disabled,
    )

# Order of items page
with st.container():
    slist = DraggableList(compile_draggablelist())
    col1, col2 = st.columns(2)
    col2.button(
        "Preview", key="order_to_preview", on_click=lambda: change_page("preview")
    )
    col1.button("Input", key="order_to_input", on_click=lambda: change_page("input"))

# Dataframe preview and download
with st.container():
    if st.session_state.page == "preview":
        df = generate_data_in_dataframe(slist)

        csv, excel, pickle = generate_download_files(df)

        col1, col2, col3 = st.columns(3)
        col1.download_button("Download CSV", data=csv, file_name="Dataset.csv")
        col2.download_button("Download Excel", data=excel, file_name="Dataset.xlsx")
        col3.download_button("Download Pickle", data=pickle, file_name="Dataset.pkl")
        st.dataframe(df.head(), hide_index=True, use_container_width=True)

        st.button(
            "Change order",
            key="preview_to_order",
            on_click=lambda: change_page("order"),
        )
        st.button(
            "Change input",
            key="preview_to_input",
            on_click=lambda: change_page("input"),
        )
