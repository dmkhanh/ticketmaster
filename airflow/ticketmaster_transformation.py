import os
from datetime import datetime
from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig
from pathlib import Path

project_config = ProjectConfig("/usr/local/airflow/dags/dbt/ticketmaster")

profile_config = ProfileConfig(
    profile_name="template_by_vitlamdata",
    target_name="dev",
    profiles_yml_filepath=Path('/usr/local/airflow/dags/dbt/ticketmaster/profiles.yml')
)

@dag(
    dag_id="ticketmaster_transformation_v01",
    schedule_interval="@daily",
    start_date=datetime(2023, 10, 10),
    catchup=False,
)

def etl_to_postgres():
    
    load_data = BashOperator(
        task_id='ingest_data',
        bash_command='python3 /usr/local/airflow/include/ingest_data.py'
    )

    transform_data = DbtTaskGroup(
        project_config=project_config,
        profile_config=profile_config,
        execution_config=ExecutionConfig(
            dbt_executable_path=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"
        )
    )

    load_data >> transform_data

etl_to_postgres()