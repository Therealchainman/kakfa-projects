from confluent_kafka.admin import AdminClient, NewPartitions

BOOTSTRAP_SERVER = 'localhost:9092'
TOPIC = 'purchases'
NEW_PARTITIONS_COUNT = 10

config = {
    "bootstrap.servers": BOOTSTRAP_SERVER
}

admin_client = AdminClient(config)

metadata = admin_client.list_topics(timeout = 10)
print("list of topics created: ", list(metadata.topics.keys()))
topic_metadata = metadata.topics.get(TOPIC)

if topic_metadata is None:
    print(f"Topic {TOPIC} does not exist.")
else:
    num_partitions = len(topic_metadata.partitions)
    print(f"Number of partitions for topic '{TOPIC}': {num_partitions}")
    # if NEW_PARTITIONS_COUNT > num_partitions:
    #     new_partitions = [NewPartitions(TOPIC, NEW_PARTITIONS_COUNT)]
        
    #     futures = admin_client.create_partitions(new_partitions)

    #     for topic, future in futures.items():
    #         try:
    #             future.result()
    #             print(f"Successfully increased the number of partitions for topic '{topic}' to {NEW_PARTITIONS_COUNT}.")
    #         except Exception as e:
    #             print(f"Failed to increase partitions for topic '{topic}': {e}")
    # else:
    #     print(f"New partition count must be greater than the current partition count ({num_partitions}).")