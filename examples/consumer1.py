from confluent_kafka import Consumer, KafkaException
import socket

# Configuration for Kafka consumer
conf = {
    "bootstrap.servers": "localhost:9092", # Kafka broker
    "group.id": "loan_group", # Consumer group ID
    "auto.offset.reset": "earliest", # Start reading at the earliest message
    'client.id': socket.gethostname() # Client ID
}


# Create Kafka Consumer instance
consumer = Consumer(conf)

topic = "loan1"

# Subscribe to the topic
consumer.subscribe([topic])

# Consume messages from the topic
try:
    while True:
        msg = consumer.poll(timeout = 1.0) # Poll for new messages
        if msg is None: continue # No new message
        if msg.error(): raise KafkaException(msg.error())
        print(f"Received message: {msg.value().decode('utf-8')}")
except KeyboardInterrupt:
    print("Consumer interrupted.")
finally:
    consumer.close()