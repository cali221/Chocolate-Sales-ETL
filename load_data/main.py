from scripts.ingest import load_csv
from scripts.clean import clean_data
from scripts.load_to_db import load_to_db
from scripts.transform_db import transform_and_check

# get dataframe from CSV
df = load_csv()

# get cleaned dataframe
cleaned_df = clean_data(df)

# load cleaned dataframe to database
load_to_db(cleaned_df)

# TODO: move to transform service
# transform DB schema and check results
#transform_and_check("sql_scripts/setup.psql", "sql_scripts/tests.psql")