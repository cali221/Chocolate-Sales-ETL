import pandas as pd

def load_csv(csvFile):
    """
    get dataframe from CSV file
    """
    return pd.read_csv(csvFile)