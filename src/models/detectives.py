import pandas as pd

class Detective:
    def __init__(self):
        self.detective_df = pd.read_csv("data/detectives.csv")
        
    def get_detectives(self):
        return self.detective_df

def get_csv_data(file_path):
    """
    Function to get CSV data using pandas.
    
    Args:
    file_path (str): The path to the CSV file.
    
    Returns:
    pd.DataFrame: The data from the CSV file as a pandas DataFrame.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except pd.errors.EmptyDataError:
        print(f"No data: {file_path}")
        return None
    except pd.errors.ParserError:
        print(f"Parsing error: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    file_path = "data/detectives.csv"
    data = get_csv_data(file_path)
    if data is not None:
        print(data.head())