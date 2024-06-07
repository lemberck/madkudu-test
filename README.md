# get_recent_customers.py

## Overview

`get_recent_customers.py` is a Python script designed to read customer data from a CSV file, validate the data using Pydantic, filter out customers who signed up more than a year ago, and save the filtered data to a new CSV file. The script uses logging for error handling and debugging, and dynamically generates the output file name based on the input file name.

## Features

- **Dynamic File Input and Output**: The script prompts the user to enter the input CSV file name and generates the output file name based on the input file name.
- **Data Validation**: Utilizes Pydantic for validating customer data, ensuring data integrity.
- **Logging**: Uses Loguru for comprehensive logging, including info, debug, warning, error, and critical messages.
- **Data Filtering**: Filters out customers who signed up more than a year ago from the current date.

## Requirements

This project uses Poetry for dependency management. Ensure you have Poetry installed. The dependencies are specified in the `pyproject.toml` file as follows:

```toml
[tool.poetry.dependencies]
python = "^3.10"
pandas = "^2.2.2"
loguru = "^0.7.2"
pydantic = "^2.7.3"
```

## Installation

1. Clone the repository or download the script `get_recent_customers.py`.
2. Ensure you have Poetry installed. You can install Poetry by following the instructions [here](https://python-poetry.org/docs/#installation).
3. Navigate to the project directory and install the dependencies using Poetry:
   ```bash
   poetry install --no-root
   ```

### Usage

1. Ensure you have a CSV file with customer data. You can use the provided `test-data.csv` to test the script.

2. Run the script:
   ```bash
   poetry run python get_recent_customers.py
3. Enter the path to the input CSV file when prompted (e.g., the provided test-data.csv):
```bash
Enter the path to the input CSV file: test-data.csv
```

The script will process the data and save the filtered results to a new file named proc__{original-file-name}.csv.