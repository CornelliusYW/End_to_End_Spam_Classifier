import airflow
from airflow import DAG
from airflow.operators.python_operator import ShortCircuitOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

# Define the default DAG arguments
default_args = {
    'owner': 'cornellius',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def condition_check(ti):
    # Retrieve the result of the condition check from XCom
    condition_result = ti.xcom_pull(task_ids='condition_check_drift', key='return_value')
    # Convert the result from string to boolean if necessary
    condition_result = condition_result.lower() == 'true'
    return condition_result

# Define the DAG
dag = DAG(
    'spam_classifier_monthly_model_retraining',
    default_args=default_args,
    description='A DAG that checks for data drift monthly and conditionally retrains a model',
    schedule_interval='0 0 7 * *',  # At 00:00 on day-of-month 1.
    catchup=False
)

# Task to check the condition using DockerOperator
drift_check_task = DockerOperator(
    task_id='condition_check_drift',
    image='drift_detection_env:1.0',
    api_version='auto',
    auto_remove=True,
    command="python /opt/airflow/scripts/project_spam_classifier/model_retrain.py",
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    do_xcom_push=True,
    dag=dag,
    mounts=["./docker_airflow/scripts:/opt/airflow/scripts"]
    
)

# ShortCircuitOperator to decide whether to proceed
retraining_decision = ShortCircuitOperator(
    task_id='retraining_decision',
    python_callable=condition_check,
    provide_context=True,
    dag=dag,
)

# Task to run if the condition is True
model_retrain_task = DockerOperator(
    task_id='model_retrain_task',
    image='drift_detection_env:1.0',
    api_version='auto',
    auto_remove=True,
    command="python /opt/airflow/scripts/project_spam_classifier/model_retrain.py",
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    dag=dag,
    mounts=["./docker_airflow/scripts:/opt/airflow/scripts"]
)

# Set the task dependencies
drift_check_task >> retraining_decision >> model_retrain_task

