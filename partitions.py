from confluent_kafka.admin import AdminClient, NewPartitions

BOOTSTRAP_SERVER = 'localhost:9092'
TOPIC = 'purchases'
NEW_PARTITIONS_COUNT = 5  # Set the new number of partitions

# Initialize AdminClient
admin_client = AdminClient({
    "bootstrap.servers": BOOTSTRAP_SERVER
})

# Get the current topic metadata
metadata = admin_client.list_topics(timeout=10)

# Check if the topic exists
if TOPIC not in metadata.topics:
    print(f"Topic {TOPIC} does not exist.")
else:
    # Fetch the current number of partitions for the topic
    current_partitions = len(metadata.topics[TOPIC].partitions)

    # Only increase partitions if the new count is greater than the current one
    if NEW_PARTITIONS_COUNT > current_partitions:
        # Create a NewPartitions object to specify the new partition count
        new_partitions = [NewPartitions(TOPIC, NEW_PARTITIONS_COUNT)]

        # Request the increase in partitions
        futures = admin_client.create_partitions(new_partitions)

        # Wait for operation to complete
        for topic, future in futures.items():
            try:
                future.result()  # Block until the operation is complete
                print(f"Successfully increased the number of partitions for topic '{topic}' to {NEW_PARTITIONS_COUNT}.")
            except Exception as e:
                print(f"Failed to increase partitions for topic '{topic}': {e}")
    else:
        print(f"New partition count must be greater than the current partition count ({current_partitions}).")
