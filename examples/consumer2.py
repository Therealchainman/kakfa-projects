from confluent_kafka import Consumer

BOOTSTRAP_SERVER = "localhost:29092"
GROUP_ID = "kafka-python-getting-started"

def assignment_callback(consumer, partitions):
    for p in partitions:
        print(f"Assigned to {p.topic}, partition {p.partition}, offset {p.offset}")
    consumer.assign(partitions)  # Ensure partitions are assigned

def output_metadata(consumer):
    metadata = consumer.list_topics(timeout = 10)
    print("cluster_id", metadata.cluster_id)
    print("controller_id", metadata.controller_id)
    print("brokers", metadata.brokers)
    print("topics", metadata.topics)
    print("orig_broker_id", metadata.orig_broker_id)
    print("orig_broker_name", metadata.orig_broker_name)

if __name__ == "__main__":
    config = {
        "bootstrap.servers": BOOTSTRAP_SERVER,
        "group.id": GROUP_ID,
        "auto.offset.reset": "earliest"
    }

    consumer = Consumer(config)

    output_metadata(consumer)

    topic = "purchases"
    consumer.subscribe([topic], on_assign = assignment_callback, on_revoke = assignment_callback, on_lost = assignment_callback)

    try:
        while True:
            # pass
            msg = consumer.poll(1.0)
            if msg is None:
                print("Waiting...")
            elif msg.error():
                print(f"ERROR: {msg.error()}")
            else:
                print(f"Consumed event from topic {msg.topic()}: key = {msg.key().decode('utf-8')} value = {msg.value().decode('utf-8')}")
                print(f"Partition: {msg.partition()}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()