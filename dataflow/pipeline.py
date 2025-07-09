import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import yaml
import json

#  Data Masking Logic
def mask_data(record):
    record['name'] = '****'
    record['ssn'] = 'XXX-XX-XXXX'
    return record

#  Pipeline options
class StreamOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument('--config_path', type=str, help='Path to config.yaml')

#  Pipeline Execution
def run():
    options = StreamOptions(streaming=True)
    config_path = options.config_path or 'dataflow/config.yaml'

    with open(config_path) as f:
        config = yaml.safe_load(f)

    topic = config['pubsub']['topic']
    table = config['bigquery']['output_table']
    schema = config['schema']

    p = beam.Pipeline(options=options)

    (
        p
        | 'Read PubSub' >> beam.io.ReadFromPubSub(topic=topic)
        | 'Parse JSON' >> beam.Map(lambda x: json.loads(x.decode('utf-8')))
        | 'Mask PII Fields' >> beam.Map(mask_data)
        | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
            table=table,
            schema=schema,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
        )
    )

    p.run().wait_until_finish()

if __name__ == "__main__":
    run()