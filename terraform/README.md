bq_dataset :  getwellsoon_dataset

GCS bucket: getwellsoon-bucket

Project ID :  gcp-agent-garden

pub_sub_topic:  getwellsoon-topic

region:  europe-west1

# schema = file("${path.module}/bq_schema.json")

project-root/
│
├── sample_customer.json 
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── dataflow/
│   ├── pipeline.py
│   ├── requirements.txt
│   └── metadata.json
|   |__ config.yaml
├── tests/
│   └── pubsub_publisher.py
├── composer_dags/
│   └── batch_dag.py
└── cicd/
    └── cloudbuild.yml
