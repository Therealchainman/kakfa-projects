#!/usr/bin/env python
import random
from confluent_kafka import Producer

BOOTSTRAP_SERVER = "localhost:29092"


if __name__ == "__main__":
    
    config = {
        "bootstrap.servers": BOOTSTRAP_SERVER,
        "acks": "all"
    }

    producer = Producer(config)

    def delivery_callback(err, msg):
        if err:
            print(f"ERROR: Message failed deliversy: {err}")
        else:
            partition = msg.partition()
            print(f"Produced event to topic {msg.topic()}: key = {msg.key().decode('utf-8')}, value = {msg.value().decode('utf-8')}, partition = {partition}")

    topic = "purchases"
    user_ids = ["eabara", "jsmith", "sgarcia", "jbernard", "htanaka", "awalther"]
    products = ["book", "alarm clock", "t-shirts", "gift card", "batteries"]

    count = 0
    for _ in range(10):
        user_id = random.choice(user_ids)
        product = random.choice(products)
        producer.produce(topic, product, user_id, callback = delivery_callback)
        count += 1
    producer.poll(10_000)
    producer.flush()