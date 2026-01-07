Real-Time Financial Event Intelligence System
'''
docker run -d --name zookeeper -p 2181:2181 zookeeper

docker run -d --name kafka -p 9092:9092 -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 --link zookeeper wurstmeister/kafka

docker exec -it kafka kafka-topics.sh --create --topic Financial_news --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1  --config cleanup.policy=compact

docker exec -it kafka kafka-topics.sh --list --bootstrap-server localhost:9092   

docker ps 
'''