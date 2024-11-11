from confluent_kafka import Producer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
import time

SCHEMA_REGISTRY_URL = "http://localhost:8081"

sr_config = {
    "url": SCHEMA_REGISTRY_URL
}

BOOTSTRAP_SERVER = "localhost:29092"
    
config = {
    "bootstrap.servers": BOOTSTRAP_SERVER,
    "acks": "all"
}


class Temperature:
    def __init__(self, city, reading, unit, timestamp):
        self.city = city
        self.reading = reading
        self.unit = unit
        self.timestamp = timestamp

schema_str = """{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Temperature",
    "description": "Temperature sensor reading",
    "type": "object",
    "properties": {
      "city": {
        "description": "City name",
        "type": "string"
      },
      "reading": {
        "description": "Current temperature reading",
        "type": "number"
      },
      "unit": {
        "description": "Temperature unit (C/F)",
        "type": "string"
      },
      "timestamp": {
        "description": "Time of reading in ms since epoch",
        "type": "number"
      }
    }
  }"""

def temp_to_dict(temp, ctx):
    return {"city": temp.city,
            "reading": temp.reading,
            "unit": temp.unit,
            "timestamp": temp.timestamp}

data = [Temperature('London', 12, 'C', round(time.time()*1000)),
        Temperature('Chicago', 63, 'F', round(time.time()*1000)),
        Temperature('Berlin', 14, 'C', round(time.time()*1000)),
        Temperature('Madrid', 18, 'C', round(time.time()*1000)),
        Temperature('Phoenix', 78, 'F', round(time.time()*1000))]

def delivery_report(err, event):
    if err is not None:
        key = event.key().decode("utf8")
        print(f"Delivery failed on reading for {key}: {err}")
    else:
        key = event.key().decode("utf8")
        topic = event.topic()
        partition = event.partition()
        print(f"Reading for {key} successfully produced to {topic}[{partition}]")

if __name__ == "__main__":
    topic = "temp_readings"
    schema_registry_client = SchemaRegistryClient(sr_config)

    json_serializer = JSONSerializer(schema_str,
                                     schema_registry_client,
                                     temp_to_dict)
    producer = Producer(config)
    for temp in data:
        producer.produce(topic = topic,
                         key = str(temp.city),
                         value = json_serializer(temp,
                        SerializationContext(topic, MessageField.VALUE)),
                        on_delivery = delivery_report)
    producer.flush()