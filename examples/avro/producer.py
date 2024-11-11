import os
from uuid import uuid4
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

class User:
    """
    User record

    Args:
        name (str): User's name

        favorite_number (int): User's favorite number

        favorite_color (str): User's favorite color

        address(str): User's address; confidential
    """

    def __init__(self, name, favorite_number, favorite_color):
        self.name = name
        self.favorite_number = favorite_number
        self.favorite_color = favorite_color

def user_to_dict(user, ctx):
    """
    Returns a dict representation of a User instance for serialization.

    Args:
        user (User): User instance.

        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.

    Returns:
        dict: Dict populated with user attributes to be serialized.
    """

    # User._address must not be serialized; omit from dict
    return dict(name=user.name,
                favorite_number=user.favorite_number,
                favorite_color=user.favorite_color)

def delivery_report(err, msg):
    """
    Reports the failure or success of a message delivery.

    Args:
        err (KafkaError): The error that occurred on None on success.
    """
    key = msg.key()
    if err is not None:
        print(f'Delivery failed for User record {key}: {err}')
        return
    topic = msg.topic()
    partition = msg.partition()
    offset = msg.offset()
    print(f'Message delivered to {topic} [{partition}] @ offset {offset}')

def main():
    topic = "user-avro"
    schema = "user.avsc"
    with open(schema) as f:
        schema_str = f.read()
    schema_registry_conf = {
        "url": "http://localhost:8081"
    }
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    avro_serializer = AvroSerializer(
        schema_registry_client,
        schema_str,
        user_to_dict
    )
    string_serializer = StringSerializer("utf-8")
    producer_conf = {
        "bootstrap.servers": "localhost:29092"
    }
    producer = Producer(producer_conf)
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
            key = string_serializer(str(uuid4())),
            value = avro_serializer(
                user,
                SerializationContext(topic, MessageField.VALUE)
            ),
            on_delivery = delivery_report
        )
    producer.flush()

if __name__ == "__main__":
    main()

    