# Project's Description
This is a mini learning project consisting of a simple data pipeline and data visualization on a dashboard. It processes data from 2 sources:
- The dataset '[Chocolate Sales](https://www.kaggle.com/datasets/saidaminsaidaxmadov/chocolate-sales/versions/2)' which was uploaded to Kaggle by [Saidamin Saidakhmadov](https://www.kaggle.com/saidaminsaidaxmadov) and licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). In this project, the dataset is transformed using dbt into a fact table and dimension tables. Then the resulting tables are used for data visualization on the dashboard
- Online store data stored in a normalized schema which emulates an OLTP system

## Initial Inspiration
This project was inspired by the article '[Build a Complete Data Engineering Project from Scratch (Day 42–45)](https://medium.com/@lasyachowdary1703/build-a-complete-data-engineering-project-from-scratch-day-42-45-b14b74ae1586)' by [Lasya](https://medium.com/@lasyachowdary1703) on Medium. This project adapts it to a different dataset and extends it by adding:
- Docker
- dbt transformations
- Airflow DAG to run dbt transformations on a schedule
- A second source of data (dummy online store's data)
- An API for the dummy online store implemented using FastAPI
- An OLTP database schema for the dummy online store
- Database triggers for the online store's schema
- Generator for random online store's incoming data i.e. new orders created and updates on existing orders' statuses 

# Tech Stack
(Section to be written later)

# Data Pipeline
(section to be written later)

# Steps to Run 
## Requirements
- Docker
- Docker Compose
- Kaggle API key (obtained by going to your Kaggle account settings page and clicking 'Generate New Token' or using your existing token)
## Step 1
Create a ```.env.docker``` file in the root directory of this project and add the following (with your PostgreSQL user and password, and Kaggle API token instead) to the file:
```
USING_DOCKER="true"
KAGGLE_API_TOKEN="your kaggle API token here"
POSTGRES_USER="your PostgreSQL user here"
POSTGRES_PASSWORD="your PostgreSQL password here"
POSTGRES_PORT="5432"
POSTGRES_HOST="database"
POSTGRES_DB="choco_db"
API_HOST="dummy_api"
API_PORT="80"
AIRFLOW_CONN_POSTGRES_DEFAULT="postgresql://<your PostgreSQL user>:<your PostgreSQL password>@database:5432/choco_db"
```

## Step 2
- On Linux or WSL, run the following command while at the root of this project:
    ```
    echo -e "AIRFLOW_UID=50000
    DOCKER_GID=$(getent group docker | cut -d: -f3)
    HOST_GID=$(id -g)
    HOST_UID=$(id -u)" > .env
    ```

- On Windows or Mac, create a .env file at the root of this project and add:
    ```
    AIRFLOW_UID=50000
    ```
    
## Step 3
- Run ```docker compose up``` to run without starting online store data generator run
- Run ```docker compose --profile with_online_store_sim up``` to run with the generator 
   
Make sure port 5433 is free on the host.<br>
Note that if you run without the online store data generator and don't add the data manually the charts for online store data will be empty

## Step 4 (Optional)
Once the db_setup and dummy_api services are up, you can add order or status update data for the online store manually by running SQL queries or by using the API endpoints at http://127.0.0.1:8000/docs by using the 'Try it out' button under the following POST or PATCH endpoints:
![screenshot of create order endpoint](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/api-create-order-endpoint.png?raw=true) 
![screenshot of update order endpoint](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/api-patch-order-status-endpoint.png?raw=true) <br>
You can also find relevant data from the database by using the 'Try it out' button under the GET endpoints.

## Step 5
Wait until Airflow finished starting up (it might take a while) and view the web UI at http://127.0.0.1:8081/. Login using the following credentials:
```
Username: airflow
Password: airflow
```
You can view the DAG by going to the Dags tab as shown below:<br>
![screenshot of the Dags tab on Airflow's web UI showing the dag in completed state](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/airflow-dags.png?raw=true)

## Step 6
Once Airflow has finished its first DAG run, the data marts are now available to use for data visualization. Open the dashboard at http://localhost:8501/ to view the charts

# Dashboard screenshots
(Section to be updated later)<br>
The dashboard consists of 10 charts in total with 5 automatially refreshing charts for the online store data and 5 interactive charts for the sales people's sales data as shown below
## Charts for Online Store Data
Please note that since the online store data generator generates random data including status updates with short intervals in-between, the data shown might seem unrealistic.

![screenshot of a line chart showing hourly order count in the last 24 hours](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-6.png?raw=true) 

![screenshot of a line chart showing hourly revenue in the last 24 hours](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-7.png?raw=true) 

![screenshot of a bar chart showing comparison of quantities ordered between products sold in online store (all time)](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-8.png?raw=true) 

![screenshot of a bar chart showing the average orders' status transition durations for online orders (all time)](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-9.png?raw=true) 

![screenshot of a bar chart showing the top 5 customers' countries that made the highest number of orders (all time)](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-10.png?raw=true) 

## Charts for Historical Sales People's Sales Data
![screenshot of a pie chart comparing the number of boxes shipped in different countries](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-1.png?raw=true) 

![screenshot of a line chart comparing the number of boxes shipped over time within a selected date range in selected countries](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-2.png?raw=true) 

![screenshot of a bar chart comparing the number of boxes shipped for different products according to selected date range and countries](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-3.png?raw=true) 

![screenshot of a bar chart comparing the sales amount obtained from different products according to selected date range and countries](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-4.png?raw=true) 

![screenshot of a line chart showing the number of boxes shipped attributed to selected sales people over time within selected date range](https://github.com/cali221/Chocolate-Sales-ETL/blob/main/readme-images/dashboard-5.png?raw=true) 