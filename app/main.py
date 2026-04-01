from app.scripts.ingest import load_csv
from app.scripts.clean import clean_data
from app.scripts.load_to_db import load_to_db
from app.scripts.transform_db import transform_and_check

# get dataframe from CSV
df = load_csv()

# get cleaned dataframe
cleaned_df = clean_data(df)

# load cleaned dataframe to database
load_to_db(cleaned_df)

# transform DB schema and check results
transform_and_check("app/sql_scripts/setup.psql", "app/sql_scripts/tests.psql")