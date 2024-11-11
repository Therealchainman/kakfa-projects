# notes


## Set up kafka 

This is done on linux operating system. 

This was built on linux operating system with docker version 24.0.7, and Docker Compose version 2.24.6+ds1-0ubuntu2

```sh
# docker pull apache/kafka:3.8.0
# docker pull confluentinc/cp-schema-registry:7.7.1
docker compose up -d
docker compose down
```

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

What is Telnet?
Telnet is a network protocol used for simple, text-based communication over TCP (Transmission Control Protocol). It is one of the oldest protocols used to establish interactive communication sessions between computers, especially for remote login and command execution.
Telnet allows you to manually interact with a service by opening a raw TCP connection to a specific port on a server. It is typically used for testing network connectivity or interacting with services that don’t use a web-based interface.
Why Telnet in the Kafka context? Kafka brokers, including the controller, operate over TCP connections, not HTTP. When you use telnet (or curl telnet://), you're opening a raw connection to test if a Kafka broker or controller is listening on the expected port, such as 9092 for Kafka’s broker-to-broker communication.

```sh
curl -v telnet://localhost:9092
```

2. Use Kafka REST Proxy (if available)
If you're using Confluent Kafka or have a Kafka REST Proxy set up, you can use curl to interact with Kafka through HTTP.

Here’s an example of how to fetch the metadata of a topic via Kafka REST Proxy:

```sh
curl -X GET http://localhost:9092/topics/purchases
```

Guidelines for using ports for kafka multi cluster setup. 

0–1023: Well-known ports (reserved for system or privileged services, e.g., HTTP (80), HTTPS (443), etc.). These should generally be avoided unless you're running a service that explicitly requires it.

1024–49151: Registered ports (commonly used for user-level applications and services). You can safely use ports in this range for Kafka brokers or other services.

49152–65535: Dynamic/private ports (used for temporary, ephemeral connections such as client-side ports in network communication). These are typically not used for service listening ports like Kafka brokers.

can I monitor with streamlit? 

