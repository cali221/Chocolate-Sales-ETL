from scripts.ingest import load_csv
from scripts.clean import clean_data
from scripts.load_to_db import load_to_db
from scripts.transform_db import transform_db_schema

# get dataframe from CSV
df = load_csv()

# get cleaned dataframe
cleaned_df = clean_data(df)

# load cleaned dataframe to database
load_to_db(cleaned_df)

transform_db_schema("sql_scripts/setup.psql")