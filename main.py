from scripts.ingest import load_csv
from scripts.clean import clean_data
from scripts.load_to_db import load_to_db

# get dataframe from CSV
df = load_csv('data/choco-sales.csv')

# get cleaned dataframe
cleaned_df = clean_data(df)

# load cleaned dataframe to database
load_to_db(cleaned_df)