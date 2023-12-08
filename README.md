# RandomInfoGenerator

# Project Name: Data Synthesizer

## Description

The **Data Synthesizer** is a Streamlit-based tool that allows users to generate synthetic datasets with customizable columns. It provides a user-friendly interface for selecting fields, defining column labels, and specifying data formats. The tool is designed to streamline the process of creating synthetic datasets for testing, analysis, or other purposes.

## Table of Contents
- [Key Features](#key-features)
- [Project Structure and File Usage](#project-structure-and-file-usage)
- [`main.py`](#mainpy)
- [`generator.py`](#generatorpy)
- [Installation](#installation)
- [Usage](#usage)

### Key Features

- **Interactive Selection:** Users can interactively toggle the selection of fields from a predefined list using the Streamlit web interface.

- **Custom Data Generation:** Define column labels and formats for custom data, allowing users to specify the structure and content of additional columns in the synthetic dataset.

- **Draggable Ordering:** The application provides a draggable list interface, allowing users to easily reorder both the selected and custom fields. This intuitive feature enhances the flexibility of arranging columns in the desired order.

- **Preview and Download:** After configuring the selections and custom data, users can generate a preview DataFrame to visualize the synthetic dataset. Additionally, the application offers the ability to download the generated synthetic datasets in various formats, including CSV, Excel, and Pickle.

### Project Structure and File Usage

This **Data Synthesizer** project is structured using two main Python files: `main.py` and `generator.py`. Each file serves a distinct purpose in the overall functionality of the application.

#### `main.py`

The primary entry point of the application, `main.py` handles the user interface, interaction flow, and overall orchestration of the synthetic data generation process. Key functionalities include:

- **User Interface Logic:** Defines the Streamlit app layout, interactive components, and transitions between different pages (input, order, preview).

- **Session State Management:** Utilizes Streamlit's session state to maintain a consistent state across multiple interactions and transitions within the application.

- **Data Visualization:** Displays the synthetic dataset preview and provides download buttons for various file formats (CSV, Excel, Pickle).

- **CSS Styling:** Incorporates CSS styling for different pages, enhancing the visual appeal and user experience.

- **File Output:** Provides functions to generate BytesIO objects for CSV, Excel, and Pickle files, enabling seamless file downloads.

#### `generator.py`

The `generator.py` file encapsulates the data generation logic, creating synthetic datasets based on user-defined parameters. Key functionalities include:

- **Faker Library Integration:** Utilizes the Faker library to generate realistic synthetic data for selected fields.

- **Custom Data Generation:** Implements a custom data generation function, allowing users to define column labels and formats for additional custom data columns.

- **DataFrame Generation:** Combines selected and custom data to create a synthetic DataFrame, handling exceptions related to user input errors.

This modular separation of concerns enhances code readability, maintainability, and encourages future scalability by allowing for easier modifications or additions to specific components.




## Installation

To run the **Data Synthesizer** as a Streamlit web app, ensure you have Python and the required dependencies installed. Use the following steps:

1. Clone the repository: `git clone <repository-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `streamlit run main.py`

**Note:** The Data Synthesizer is designed to be run using [Streamlit](https://streamlit.io/), a Python library for creating web applications with minimal effort. When you run the application using the `streamlit run` command, it launches a local web server and opens the app in your default web browser.

If you haven't installed Streamlit previously, you can install it via `pip`:

```bash
pip install streamlit
```

## Usage

1. **Select Fields:** Choose fields from the predefined list.
2. **Define Labels and Formats:** Provide column labels and data formats.
3. **Order Fields:** Reorder fields using the draggable list.
4. **Generate Dataset:** Click "Preview" to preview and download the synthetic dataset.
