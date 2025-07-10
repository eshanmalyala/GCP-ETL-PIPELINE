from airflow import models
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.operators.cloud_build import CloudBuildCreateBuildOperator
from airflow.utils.dates import days_ago
from google.cloud.devtools import cloudbuild_v1

# Configs
PROJECT_ID = "gcp-agent-garden"
BUCKET_NAME = "getwellsoon-bucket-11"
REGION = "us-central1"
DATASET = "getwellsoon_dataset"
TABLE = "employee"
GCS_CSV_PATH = f"gs://{BUCKET_NAME}/employe_data.csv"
GCS_JSON_PATH = f"gs://{BUCKET_NAME}/bq.json"
GCS_UDF_PATH = f"gs://{BUCKET_NAME}/udf.js"
TEMP_LOCATION = "gs://myworkspace-579raj/temp/"
RECO_TABLE = f"{PROJECT_ID}.{DATASET}.{TABLE}"

default_args = {
    "start_date": days_ago(1),
}

with models.DAG(
    "dataflow_cloudbuild_reconciliation_pipeline",
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    description="Runs Dataflow via Cloud Build and validates row counts",
) as dag:

    # Step 1: Upload files to GCS (if needed)
    upload_files = BashOperator(
        task_id="upload_files",
        bash_command=f"""
        gsutil cp /home/airflow/gcs/data/dataflow-batch-job/* gs://{BUCKET_NAME}/
        """
    )

    # Step 2: Trigger Cloud Build that runs Dataflow job
    build_body = {
        "steps": [
            {
                "name": "gcr.io/google.com/cloudsdktool/cloud-sdk",
                "entrypoint": "bash",
                "args": [
                    "-c",
                    f"""
                    gcloud dataflow jobs run dataflow-pii-reco-job-{{{{ ts_nodash }}}} \
                      --gcs-location gs://dataflow-templates-europe-west1/latest/GCS_Text_to_BigQuery \
                      --region {REGION} \
                      --staging-location {TEMP_LOCATION} \
                      --parameters inputFilePattern={GCS_CSV_PATH},JSONPath={GCS_JSON_PATH},outputTable={RECO_TABLE},bigQueryLoadingTemporaryDirectory={TEMP_LOCATION},javascriptTextTransformGcsPath={GCS_UDF_PATH},javascriptTextTransformFunctionName=transform
                    """
                ]
            }
        ],
        "timeout": "1200s",  # Optional
    }

    trigger_dataflow = CloudBuildCreateBuildOperator(
        task_id="trigger_dataflow_via_cloudbuild",
        project_id=PROJECT_ID,
        build=build_body
    )

    # Step 3: Reconciliation Task - compare row count
    reconciliation_query = f"""
        DECLARE input_count INT64;
        DECLARE bq_count INT64;

        SET input_count = (
            SELECT COUNT(*) FROM EXTERNAL_QUERY(
                "projects/{PROJECT_ID}/locations/{REGION}/connections/gcs_connection",
                "SELECT * FROM `{GCS_CSV_PATH}`"
            )
        );

        SET bq_count = (
            SELECT COUNT(*) FROM `{RECO_TABLE}`
        );

        SELECT
            input_count AS input_file_rows,
            bq_count AS bigquery_table_rows,
            IF(input_count = bq_count, "MATCH", "MISMATCH") AS reconciliation_result;
    """

    reconciliation = BigQueryInsertJobOperator(
        task_id="reconciliation_check",
        configuration={
            "query": {
                "query": reconciliation_query,
                "useLegacySql": False,
            }
        },
        location=REGION,
        project_id=PROJECT_ID,
    )

    # DAG Flow
    upload_files >> trigger_dataflow >> reconciliation
