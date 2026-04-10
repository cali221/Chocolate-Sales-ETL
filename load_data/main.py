from scripts.ingest import load_csv
from scripts.clean import clean_data
from scripts.load_to_db import load_to_db
from scripts.transform_db import transform_and_check

# get dataframe from CSV
df = load_csv()

# load cleaned dataframe to database
load_to_db(df)