from confluent_kafka import Producer
import socket

# Configuration for Kafka producer
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker
    'client.id': socket.gethostname() # Client ID
}

# Create Producer instance
producer = Producer(conf)

# Delivery callback for producer confirmation
def delivery_report(err, msg):
    """ Called once for each message to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Send some messages
topic = "loan1"

for i in range(10):
    message = f"Message {i}"
    producer.produce(topic, value=message, callback=delivery_report)

# Wait for any outstanding messages to be delivered
producer.flush()
