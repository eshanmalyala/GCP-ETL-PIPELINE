from airflow import DAG
from airflow.providers.google.cloud.operators.dataflow import DataflowStartFlexTemplateOperator
from datetime import datetime

with DAG(
    'batch_customer_masking',
    start_date=datetime(2025, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    run_batch = DataflowStartFlexTemplateOperator(
        task_id='launch_batch_masking',
        project_id='gcp-agent-garden',
        location='europe-west1',
        body={
            "launch_parameter": {
                "jobName": "batch-mask-job",
                "containerSpecGcsPath": "gs://getwellsoon-bucket/templates/streaming_template.json",
                "parameters": {
                    "config_path": "dataflow/config.yaml"
                }
            }
        }
    )