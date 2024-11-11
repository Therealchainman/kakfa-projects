from user_pb2 import User
from uuid import uuid4
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer


def delivery_report(err, msg):
    """
    Reports the failure or success of a message delivery.
    
    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    """
    key = msg.key()
    if err is not None:
        print(f"Delivery failed for User record {key}: {err}")
        return
    topic = msg.topic()
    partition = msg.partition()
    offset = msg.offset()
    print(f"User record {key} successfully produced to {topic} [{partition}] at offset {offset}")

def main():
    topic = "protobuf_topic"
    schema_registry_conf = {
        "url": "http://localhost:8081"
    }
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    string_serializer = StringSerializer("utf_8")
    protobuf_serializer = ProtobufSerializer(
        User,
        schema_registry_client,
        {"use.deprecated.format": False}
    )
    producer_conf = {
        "bootstrap.servers": "localhost:29092"
    }
    producer = Producer(producer_conf)
    print(f"Producing user records to topic {topic}. ^C to exit.")
    users = [
        User(name = "Alice", 
             favorite_number = 42, 
             favorite_color = "blue"),
        User(name = "Bob",
            favorite_number = 24,
            favorite_color = "red"),
        User(name = "Charlie",
            favorite_number = 100,
            favorite_color = "green"),
        User(name = "David",
            favorite_number = 0,
            favorite_color = "yellow"),
        User(name = "Eve",
            favorite_number = 1,
            favorite_color = "black")
    ]
    for user in users:
        producer.poll(1.0)
        producer.produce(
            topic = topic,
            partition = 0,
            key = string_serializer(str(uuid4())),
            value = protobuf_serializer(
                user,
                SerializationContext(topic, MessageField.VALUE)
            ),
            on_delivery = delivery_report
        )
    producer.flush()

if __name__ == "__main__":
    main()