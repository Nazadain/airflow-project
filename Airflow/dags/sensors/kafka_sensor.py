from airflow.sensors.base import BaseSensorOperator
from airflow.utils.decorators import apply_defaults
from confluent_kafka import Consumer, KafkaException, TopicPartition


class KafkaMessageSensor(BaseSensorOperator):
    @apply_defaults
    def __init__(self, topic, kafka_server, group_id="airflow-kafka-sensor", keyword=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.topic = topic
        self.kafka_server = kafka_server
        self.group_id = group_id
        self.keyword = keyword

    def poke(self, context):
        print(f"KafkaSensor: Checking topic '{self.topic}' for messages...")
        conf = {
            'bootstrap.servers': self.kafka_server,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest'
        }

        consumer = None
        try:
            consumer = Consumer(conf)
            tp = TopicPartition(self.topic, 0, 0)
            consumer.assign([tp])
            consumer.subscribe([self.topic])



            print("Waiting for messages...")

            while True:
                msg = consumer.poll(timeout=10.0)

                if msg is None:
                    continue

                if msg.error():
                    raise KafkaException(msg.error())

                break

            value = msg.value().decode("utf-8")
            print(f"KafkaSensor: Received message: {value}")

            if self.keyword is None or self.keyword in value:
                print(f"KafkaSensor: Keyword '{self.keyword}' found, returning True.")
                return True
            else:
                print(f"KafkaSensor: Keyword '{self.keyword}' not found in message.")

            return False

        except KafkaException as e:
            print(f"KafkaSensor Error: {e}")

        finally:
            consumer.close()
