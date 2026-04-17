import os
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator

dag_default_arguments = {
    'owner': 'me',
    'email': 'theresiacalista57@gmail.com'
}

with DAG(dag_id='dbt_transform', 
         default_args=dag_default_arguments, 
         start_date=datetime(2026, 4, 15),
         catchup=False,
         max_active_runs=1,
         schedule=timedelta(minutes=15)) as load_kaggle_data_dag:
    load_kaggle_data_task = DockerOperator(task_id='dbt_transform',
                                           image='transform',
                                           command=["dbt", "build"],
                                           container_name='transform',
                                           docker_url='unix://var/run/docker.sock',
                                           network_mode='chocolate-sales-data-pipeline_default',
                                           mount_tmp_dir=False,
                                           auto_remove='success',
                                           environment={
                                                "USING_DOCKER": os.getenv("USING_DOCKER"),
                                                "POSTGRES_PASSWORD":os.getenv('POSTGRES_PASSWORD'),
                                                "POSTGRES_HOST":os.getenv('POSTGRES_HOST'),
                                                "POSTGRES_USER":os.getenv('POSTGRES_USER'),
                                                "POSTGRES_PORT":os.getenv('POSTGRES_PORT'),
                                                "POSTGRES_DB":os.getenv('POSTGRES_DB'),
                                                "DBT_PROJECT_DIR": "/choco-project-transform/choco_sales",
                                                "DBT_PROFILES_DIR": "/choco-project-transform/choco_sales",
                                                "DBT_ENGINE_LOG_PATH": "/choco-project-transform/choco_sales/logs",
                                                "DBT_ENGINE_TARGET_PATH": "/choco-project-transform/choco_sales/target"
                                            })
                                            