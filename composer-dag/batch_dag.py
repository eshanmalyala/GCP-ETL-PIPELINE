from airflow import models
from airflow.providers.google.cloud.operators.dataflow import DataflowTemplateOperator
from datetime import datetime

with models.DAG(
    dag_id='trigger_dataflow_dag',
    start_date=datetime(2021, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["dataflow"],
) as dag:

    run_dataflow = DataflowTemplateOperator(
        task_id="run_dataflow_template",
        template="gs://dataflow-templates-us-central1/latest/GCS_Text_to_BigQuery",
        location="us-central1",
        parameters={
            "inputFilePattern": "gs://getwellsoon-bucket-0/user.csv",
            "JSONPath": "gs://getwellsoon-bucket-0/bq.json",
            "outputTable": "gcp-agent-garden:getwellsoon_dataset.employee",
            "bigQueryLoadingTemporaryDirectory": "gs://myworkspace-579raj/",
            "javascriptTextTransformGcsPath": "gs://getwellsoon-bucket-0/udf.js",
            "javascriptTextTransformFunctionName": "transform"
        },
        gcp_conn_id='google_cloud_default'
    )
