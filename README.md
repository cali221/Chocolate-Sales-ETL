# Project's Description
This is a mini learning project, demonstrating a simple ETL pipeline where data from a CSV file is cleaned, loaded to a database, normalized and finally used for data visualization on a dashboard. 
<br><br>
This project was inspired by the article '[Build a Complete Data Engineering Project from Scratch (Day 42–45)](https://medium.com/@lasyachowdary1703/build-a-complete-data-engineering-project-from-scratch-day-42-45-b14b74ae1586)' by [Lasya](https://medium.com/@lasyachowdary1703) on Medium. This project adapts it to a different dataset and extends it by adding:
- Database normalization
- Validation checks
- Environment configuration
- More charts to visualize data

# Dataset Source
This project uses the dataset: '[Chocolate Sales](https://www.kaggle.com/datasets/saidaminsaidaxmadov/chocolate-sales/versions/2)' which was uploaded to Kaggle by [Saidamin Saidakhmadov](https://www.kaggle.com/saidaminsaidaxmadov) and licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
<br><br>
In this project, the data was used/modified in the following ways:
- The column names were modified 
- The data was cleaned
- It was normalized into database tables
<br>The dataset is not included in this repository, it can be manually downloaded from the link provided.

# Steps to Run
## Preparation:
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
## Database setup:
1. Create a database using PostgreSQL named choco-db
2. Run ```python main.py``` to load the data from the CSV file to the database
3. Run ```psql -U [your PostgreSQL username here] -d choco_db  -f sql_scripts/setup.psql``` to transform the initial table into normalized tables
## Check the results by running tests: 
Run ```psql -U [your PostgreSQL username here] -d choco_db  -f sql_scripts/tests.psql```
## View the data visualization on a dashboard:
To view the dashboard run ```streamlit run dashboard.py```

# Database Schema
After the cleaned DataFrame is loaded to the database, the following database schema was achieved:<br>
![screenshot of initial database ERD](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/initial_erd.png?raw=true)
