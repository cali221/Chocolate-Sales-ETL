# import os
# from airflow import DAG
# from datetime import datetime
# from airflow.providers.docker.operators.docker import DockerOperator
# from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator

# dag_default_arguments = {
#     'owner': 'me',
#     'email': 'theresiacalista57@gmail.com'
# }

# with DAG(dag_id='load_kaggle_data', 
#          default_args=dag_default_arguments, 
#          start_date=datetime(2026, 1, 1),
#          catchup=False,
#          schedule='@yearly') as load_kaggle_data_dag:
#     load_kaggle_data_task = DockerOperator(task_id='load_kaggle_data',
#                                            image='load_kaggle_data',
#                                            command=["python", "-m", "main"],
#                                            container_name='load_kaggle_data',
#                                            docker_url='unix://var/run/docker.sock',
#                                            network_mode='airflow_network',
#                                            mount_tmp_dir=False,
#                                            auto_remove='success',
#                                            environment={
#                                                 "USING_DOCKER": os.getenv("USING_DOCKER"),
#                                                 "POSTGRES_PASSWORD":os.getenv('POSTGRES_PASSWORD'),
#                                                 "POSTGRES_HOST":os.getenv('POSTGRES_HOST'),
#                                                 "POSTGRES_USER":os.getenv('POSTGRES_USER'),
#                                                 "POSTGRES_PORT":os.getenv('POSTGRES_PORT'),
#                                                 "POSTGRES_DB":os.getenv('POSTGRES_DB')
#                                             })
    
#     trigger_dbt_transform_task = TriggerDagRunOperator(trigger_dag_id='dbt_transform',
#                                                        task_id='trigger_dbt_transform')
    
    
#     load_kaggle_data_task >> trigger_dbt_transform_task 
                                            