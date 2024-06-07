import pandas as pd
from datetime import datetime
from loguru import logger
from pydantic import BaseModel, field_validator, ValidationError
from typing import List
import os

# Setup logging
logger.add("logs/recent_customers_{time}.log", rotation="5 days")

## Data validation
class CustomerData(BaseModel):
    """
    Pydantic model for customer data validation.
    
    Attributes:
        customer_id (int): Unique identifier for the customer.
        name (str): Name of the customer.
        signup_date (datetime): Date when the customer signed up.
        country (str): Country of the customer.
    """
    customer_id: int
    name: str
    signup_date: datetime
    country: str

    @field_validator('signup_date', mode='before')
    def parse_signup_date(cls, value):
        """
        Parse signup_date from string to datetime if necessary.
        If the value is already a datetime object, it will be returned as is.
        """
        if isinstance(value, str):
            return datetime.strptime(value, '%Y-%m-%d')
        return value

def read_csv_file(file_path: str) -> pd.DataFrame:
    """
    Reads a CSV file into a DataFrame.

    :param file_path: Path to the input CSV file.
    :return: DataFrame containing the CSV data.
    """
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Successfully read the input file: {file_path}")
        return df
    except Exception as e:
        logger.error(f"Error reading the input file: {e}")
        raise

def validate_customer_data(df: pd.DataFrame) -> List[CustomerData]:
    """
    Validates the data in the DataFrame using Pydantic.

    :param df: DataFrame containing the customer data.
    :return: List of validated CustomerData instances.
    """
    try:
        data = df.to_dict(orient='records')
        validated_data = [CustomerData(**item) for item in data]
        logger.info("Data validation successful")
        return validated_data
    except ValidationError as e:
        logger.error(f"Data validation error: {e}")
        raise

def filter_recent_customers(validated_data: List[CustomerData]) -> pd.DataFrame:
    """
    Filters out customers who signed up more than a year ago.

    :param validated_data: List of validated CustomerData instances.
    :return: DataFrame containing customers who signed up within the last year.
    """
    try:
        one_year_ago = datetime.now() - pd.DateOffset(years=1)
        filtered_data = [item.dict() for item in validated_data if item.signup_date >= one_year_ago]
        filtered_df = pd.DataFrame(filtered_data)
        logger.info("Filtered customers who signed up more than a year ago")
        return filtered_df
    except Exception as e:
        logger.error(f"Error filtering customers: {e}")
        raise

def save_filtered_data_to_csv(df: pd.DataFrame, output_file: str):
    """
    Saves the DataFrame to a CSV file.

    :param df: DataFrame containing the filtered data.
    :param output_file: Path to the output CSV file.
    """
    try:
        df.to_csv(output_file, index=False)
        logger.info(f"Successfully saved the filtered data to: {output_file}")
    except Exception as e:
        logger.error(f"Error saving the filtered data: {e}")
        raise

def main(input_file: str):
    """
    Main function to orchestrate the reading, validating, filtering, and saving process.

    :param input_file: Path to the input CSV file.
    """
    output_file = f"proc__{os.path.basename(input_file)}"
    try:
        df = read_csv_file(input_file)
        validated_data = validate_customer_data(df)
        filtered_df = filter_recent_customers(validated_data)
        save_filtered_data_to_csv(filtered_df, output_file)
    except Exception as e:
        logger.critical(f"Failed to process the CSV file: {e}")

if __name__ == "__main__":
    input_file = input("Enter the path to the input CSV file: ")
    main(input_file)
