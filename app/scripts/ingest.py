import kagglehub
from kagglehub import KaggleDatasetAdapter

def load_csv():
    """
    get dataframe from CSV file from
    """
    print("Loading CSV to a DataFrame...")
    df = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "saidaminsaidaxmadov/chocolate-sales/versions/2",
        "Chocolate Sales (2).csv",
    )
    print("Loaded CSV to a DataFrame")
    return df