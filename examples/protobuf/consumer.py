from user_pb2 import User
from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer

def main():
    topic = "protobuf_topic"
    protobuf_deserializer = ProtobufDeserializer(
        User,
        {"use.deprecated.format": False}
    )
    consumer_conf = {
        "bootstrap.servers": "localhost:29092",
        "group.id": "example_serde_protobuf",
        "auto.offset.reset": "earliest"
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])
    while True:
        try:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            user = protobuf_deserializer(
                msg.value(),
                SerializationContext(topic, MessageField.VALUE)
            )
            if user is not None:
                print(
                    f"User record {msg.key()}:\n"
                    f"\tname: {user.name}\n"
                    f"\tfavorite_number: {user.favorite_number}\n"
                    f"\tfavorite_color: {user.favorite_color}\n"
                )
        except KeyboardInterrupt:
            break
    consumer.close()

if __name__ == "__main__":
    main()