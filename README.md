# Project's Description
This is a mini learning project, demonstrating a simple ETL pipeline where data from a CSV file was converted into a DataFrame, cleaned, and loaded to a database. Then the database table was decomposed into multiple related tables to improve the database schema. Finally, the data from the database was used for data visualization on a dashboard. 
<br><br>
This project was inspired by the article '[Build a Complete Data Engineering Project from Scratch (Day 42–45)](https://medium.com/@lasyachowdary1703/build-a-complete-data-engineering-project-from-scratch-day-42-45-b14b74ae1586)' by [Lasya](https://medium.com/@lasyachowdary1703) on Medium. This project adapts it to a different dataset and extends it by adding:
- Database table decomposition to improve the database schema
- Validation checks between the initial database table and the final tables
- Environment configuration
- More charts to visualize data

# Dataset Source
This project uses the dataset: '[Chocolate Sales](https://www.kaggle.com/datasets/saidaminsaidaxmadov/chocolate-sales/versions/2)' which was uploaded to Kaggle by [Saidamin Saidakhmadov](https://www.kaggle.com/saidaminsaidaxmadov) and licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
<br><br>
In this project, the data was used/modified in the following ways after being converted into a DataFrame:
- The column names were modified 
- The data was cleaned
- It was loaded to a database as one table which was then split into multiple related tables

# Steps to Run
## Preparation
1. Create a new virtual environment in the project folder by running ```python -m venv venv```
2. Activate the virtual environment by running:
- ```venv\Scripts\activate``` for Windows Command Prompt
- ```venv\Scripts\activate.ps1``` for Windows PowerShell  
- ```source venv/bin/activate``` for Linux or macOS
3. Install the required packages by running ```pip install -r requirements.txt``` while in the root directory of this project
4. Create a .env file in the root directory of this project and add the following (with your PostgreSQL setup data instead) to the file: 
```
DB_PASSWORD="your PostgreSQL password"
DB_PORT="your PostgreSQL port"
DB_USER="your PostgreSQL username"
DB_HOST="your PostgreSQL host"
KAGGLE_API_TOKEN="your Kaggle API token"
```
## Database setup
1. Create a database using PostgreSQL named choco_db
2. Run ```python main.py``` when in the root directory of this project to load the data from the CSV file to the database and transform the schema

## Check the results by running tests 
Run ```psql -U [your PostgreSQL username here] -d choco_db -f sql_scripts/tests.psql```
## View the data visualization on a dashboard
To view the dashboard run ```streamlit run dashboard.py```

# Data Pipeline
1. The data from CSV was converted into pandas DataFrame. Then the DataFrame was cleaned and the columns were renamed
2. The DataFrame was loaded into the PostgreSQL database as a table
3. The database table is decomposed into multiple related tables with primary keys and foreign keys
4. The data from the database table is used for the dashboard for data visualization

# Results
## Database schema
After the cleaned DataFrame is loaded to the database, the following database schema with just one table was achieved:<br>
![screenshot of initial database ERD](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/initial-erd.png?raw=true) 
<br><br>
The table was then decomposed into tables representing different entities (country, sales_person, product and sales).<br>
Primary keys were introduced to ensure the uniqueness of each row and foreign keys were introduced to represent<br>
the relationships between the entities. The following database schema was obtained:<br>
![screenshot of final database ERD](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/final-erd.png?raw=true) 
<br> 
This was done to improve maintainablity, because separating the entities makes updating the data simpler and reduces<br>
the risks of inconsistent records. Additionally, it allows data, such as products or countries, to be stored independently<br>
of sales records.<br><br> 
The initial table (choco_stats) was intentionally kept in the database, so that the new tables that resulted<br>
from the decomposition can be checked against the initial table using the tests.psql script.

## Dashboard screenshots
The dashboard consists of 5 interactive charts as shown by the following screenshots:
![screenshot of a pie chart comparing the number of boxes shipped in different countries](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-1.png?raw=true) 

![screenshot of a line chart comparing the number of boxes shipped over time within a selected date range in selected countries](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-2.png?raw=true) 

![screenshot of a bar chart comparing the number of boxes shipped for different products according to selected date range and countries](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-3.png?raw=true) 

![screenshot of a bar chart comparing the sales amount obtained from different products according to selected date range and countries](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-4.png?raw=true) 

![screenshot of a line chart showing the number of boxes shipped attributed to selected sales people over time within selected date range](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-5.png?raw=true) 
