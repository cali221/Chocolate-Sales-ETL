# Project's Description
This is a mini learning project, demonstrating a simple ETL pipeline where data from a CSV file was converted into a DataFrame, cleaned, and loaded to a database. Then the database table was decomposed into multiple related tables to improve the database schema. Finally, the data from the database was used for data visualization on a dashboard. 
<br><br>
This project was inspired by the article '[Build a Complete Data Engineering Project from Scratch (Day 42–45)](https://medium.com/@lasyachowdary1703/build-a-complete-data-engineering-project-from-scratch-day-42-45-b14b74ae1586)' by [Lasya](https://medium.com/@lasyachowdary1703) on Medium. This project adapts it to a different dataset and extends it by adding:
- Database table decomposition to improve the database schema
- Validation checks
- Environment configuration
- More charts to visualize data

# Dataset Source
This project uses the dataset: '[Chocolate Sales](https://www.kaggle.com/datasets/saidaminsaidaxmadov/chocolate-sales/versions/2)' which was uploaded to Kaggle by [Saidamin Saidakhmadov](https://www.kaggle.com/saidaminsaidaxmadov) and licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
<br><br>
In this project, the data was used/modified in the following ways after being converted into a DataFrame:
- The column names were modified 
- The data was cleaned
- It was loaded to a database as one table which was then split into multiple related tables
<br>
The dataset is not included in this repository, it can be manually downloaded from the link provided.

# Steps to Run
## Preparation
1. Download the CSV file (Likely titled "Chocolate Sales (2).csv") from [here](https://www.kaggle.com/datasets/saidaminsaidaxmadov/chocolate-sales/versions/2) 
2. Create a directory called 'data' in the root directory of this project
3. Move the downloaded CSV file, likely named "Chocolate Sales (2).csv", into the data directory 
4. Rename the CSV file as 'choco-sales.csv' 
5. Install the required packages by running ```pip install -r requirements.txt``` while in the root directory of this project
6. Create a .env file in the root directory of this project and add the following (with your PostgreSQL setup data instead) to the file: 
```
DB_PASSWORD="your PostgreSQL password"
DB_PORT="your PostgreSQL port"
DB_USER="your PostgreSQL username"
DB_HOST="your PostgreSQL host"
```
## Database setup
1. Create a database using PostgreSQL named choco-db
2. Run ```python main.py``` to load the data from the CSV file to the database
3. Run ```psql -U [your PostgreSQL username here] -d choco_db -f sql_scripts/setup.psql``` to decompose the intial table into related tables
## Check the results by running tests 
Run ```psql -U [your PostgreSQL username here] -d choco_db -f sql_scripts/tests.psql```
## View the data visualization on a dashboard
To view the dashboard run ```streamlit run dashboard.py```

# Results
## Database schema
After the cleaned DataFrame is loaded to the database, the following database schema with just one table was achieved:<br>
![screenshot of initial database ERD](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/initial_erd.png?raw=true) 
<br>
The table was then decomposed into related tables representing different entities (country, sales_person, product and sales).<br> 
The following database schema was obtained:<br>
![screenshot of final database ERD](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/normalized-erd.png?raw=true) 
<br> 
The initial table (i.e. choco_stats) was intentionally kept in the database, so that the new tables that resulted from the<br>
decomposition can be checked against the initial table.

## Dashboard screenshots
![screenshot of a pie chart comparing the number of boxes shipped in different countries](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-1.png?raw=true) 

![screenshot of a line chart comparing the number of boxes shipped over time within a selected date range in selected countries](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-2.png?raw=true) 

![screenshot of a bar chart comparing the number of boxes shipped for different products according to selected date range and countries](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-3.png?raw=true) 

![screenshot of a bar chart comparing the sales amount obtained from different products according to selected date range and countries](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-4.png?raw=true) 

![screenshot of a line chart showing the number of boxes shipped attributed to selected sales people over time within selected date range](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-5.png?raw=true) 
