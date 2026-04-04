# TODO: move to dbt staging -> DONE
import pandas as pd

def clean_data(df):
    """
    clean dataframe obtained from CSV
    """
    ################# CHECK INITIAL CSV ##################################
    print("Checking initial dataframe...")
    print(f"Any null values present in DF: {df.isnull().values.any()} \n")
    print(f"Number of duplicated rows: {df.duplicated().sum()} \n");
    print(f"Unique countries: {df['Country'].unique()}")
    print(f"Unique sales person: {df['Sales Person'].unique()} \n")
    print(f"Unique products: {df['Product'].unique()} \n")
    print(f"Initial df.describe:\n{df.describe()} \n")
    print(f"Initial df.dtypes:\n{df.dtypes} \n")

    ########################## CLEAN ##########################################
    print("Cleaning dataframe ...")
    # adjust column names so columns are in the form e.g. sales_person                        -> DONE in dbt
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # changed sales amount column data from string to float                                   -> DONE in dbt
    df["amount"] = df["amount"].str.replace("$", "").str.replace(",", "").astype(float)

    # edit sales amount column name from 'amount' to 'sales_amount_usd' for clarity           -> DONE in dbt
    df.rename(columns={"amount": "sales_amount_usd"}, inplace=True)

    # adjust the sales person column data to ensure correct capitalization                    -> DONE in DBT
    # and no unnecessary whitespaces
    df["sales_person"] = df["sales_person"].str.strip().str.title()

    # ensure no unnecessary whitespaces for country column data                               -> DONE in DBT
    df["country"] = df["country"].str.strip()

    # ensure no unnecessary whitespaces for product column data                               -> DONE in DBT
    df["product"] = df["product"].str.strip()

    # convert date data from string to datetime (YYYY-mm-dd format)                           -> DONE in DBT
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")

    ################## PREVIEW ###########################
    print("Cleaned dataframe preview:")
    print(df.head())
    print('\n')
    print(f"Final df.describe:\n{df.describe()}")
    print(f"Final df.dtypes:\n{df.dtypes} \n")

    return df