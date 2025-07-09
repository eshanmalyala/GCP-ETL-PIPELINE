from google.cloud import pubsub_v1
import json

# Project and topic configuration
project_id = "gcp-agent-garden"
topic_id = "getwellsoon-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# New customer data
data = {
    "customer_id": "30051990",
    "name": "rmalyala",
    "email": "rajasekahr.malyala@capgemini.com",
    "ssn": "333-44-5555",
    "address": "Hyderabad",
    "timestamp": "2025-07-09T14:00:00Z"
}

# Publish message to Pub/Sub
future = publisher.publish(topic_path, json.dumps(data).encode("utf-8"))
print(f"Published message ID: {future.result()}")