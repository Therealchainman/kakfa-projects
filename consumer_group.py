from confluent_kafka.admin import AdminClient
import time

def describe_consumer_group(bootstrap_servers, group_id):
    admin_client = AdminClient({
        'bootstrap.servers': bootstrap_servers
    })

    future = admin_client.list_consumer_groups(request_timeout = 10)
    time.sleep(10)
    try:
        print(future)
        list_consumer_groups_result = future.result()
        print(dir(list_consumer_groups_result))
        print("valid: ", list_consumer_groups_result.valid)
        print("errors: ", list_consumer_groups_result.errors)
    except:
        raise Exception("Failed to list consumer groups")

    # # Use AdminClient to describe the consumer group
    # for group in admin_client.list_consumer_groups():
    #     print(group[0])

    
    # # Check if the consumer group exists
    # if group_id in [group.group_id for group in consumer_groups]:
    #     print(f"Consumer group '{group_id}' exists. Fetching detailed information...")
    # else:
    #     print(f"Consumer group '{group_id}' does not exist.")
    #     return

    # Describe the group
    group_description = admin_client.describe_consumer_groups([group_id], request_timeout=10)
    print(group_description)
    # for description in group_description:
    #     print(f"Group: {description.group}")
    #     print(f"State: {description.state}")
    #     print(f"Members: {len(description.members)}")
        
    #     for member in description.members:
    #         print(f"  Member ID: {member.member_id}")
    #         print(f"  Client ID: {member.client_id}")
    #         print(f"  Host: {member.client_host}")
            
    #         # Print assigned partitions
    #         if member.assignment:
    #             print(f"  Assigned partitions: {member.assignment.partitions}")
    #         else:
    #             print("  No partitions assigned.")
    
    return group_description

# Parameters
bootstrap_servers = "localhost:9092"
group_id = "kafka-python-getting-started"

# Call the function
describe_consumer_group(bootstrap_servers, group_id)