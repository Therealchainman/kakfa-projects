def example_describe_topics(a, args):
    """
    Describe Topics
    """
    include_auth_ops = bool(int(args[0]))
    args = args[1:]
    topics = TopicCollection(topic_names=args)
    futureMap = a.describe_topics(topics, request_timeout=10, include_authorized_operations=include_auth_ops)

    for topic_name, future in futureMap.items():
        try:
            t = future.result()
            print("Topic name             : {}".format(t.name))
            print("Topic id               : {}".format(t.topic_id))
            if (t.is_internal):
                print("Topic is Internal")

            if (include_auth_ops):
                print("Authorized operations  : ")
                op_string = ""
                for acl_op in t.authorized_operations:
                    op_string += acl_op.name + "  "
                print("    {}".format(op_string))

            print("Partition Information")
            for partition in t.partitions:
                print("    Id                : {}".format(partition.id))
                leader = partition.leader
                print(f"    Leader            : {leader}")
                print("    Replicas          : {}".format(len(partition.replicas)))
                for replica in partition.replicas:
                    print(f"         Replica            : {replica}")
                print("    In-Sync Replicas  : {}".format(len(partition.isr)))
                for isr in partition.isr:
                    print(f"         In-Sync Replica    : {isr}")
                print("")
            print("")

        except KafkaException as e:
            print("Error while describing topic '{}': {}".format(topic_name, e))
        except Exception:
            raise