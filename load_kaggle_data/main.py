from scripts.ingest import load_csv
from scripts.load_to_db import load_to_db

# get dataframe from CSV
df = load_csv()

# load cleaned dataframe to database
load_to_db(df)