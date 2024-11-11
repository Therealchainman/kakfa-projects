from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer

class User:
    """
    User record

    Args:
        name (str): User's name

        favorite_number (int): User's favorite number

        favorite_color (str): User's favorite color
    """

    def __init__(self, name=None, favorite_number=None, favorite_color=None):
        self.name = name
        self.favorite_number = favorite_number
        self.favorite_color = favorite_color

def dict_to_user(obj, ctx):
    """
    Converts object literal(dict) to a User instance.

    Args:
        obj (dict): Object literal(dict)

        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.
    """

    if obj is None:
        return None

    return User(name=obj['name'],
                favorite_number=obj['favorite_number'],
                favorite_color=obj['favorite_color'])

def main():
    topic = "user-avro"
    schema = "user.avsc"
    with open(schema) as f:
        schema_str = f.read()

    schema_registry_conf = {
        "url": "http://localhost:8081"
    }
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    avro_deserializer = AvroDeserializer(
        schema_registry_client,
        schema_str,
        dict_to_user
    )
    consumer_conf = {
        "bootstrap.servers": "localhost:29092",
        "group.id": "user-consumer-avro",
        "auto.offset.reset": "earliest"
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])
    while True:
        try:
            msg = consumer.poll(1.0)
            if msg is None: continue 
            user = avro_deserializer(
                msg.value(),
                SerializationContext(msg.topic(), MessageField.VALUE)
            )
            if user is not None:
                print(f"User(name = {user.name}, favorite_number = {user.favorite_number}, favorite_color = {user.favorite_color})")
        except KeyboardInterrupt:
            break
    consumer.close()

if __name__ == "__main__":
    main()