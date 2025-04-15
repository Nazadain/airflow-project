from airflow import DAG
from airflow.operators.python import PythonOperator
from confluent_kafka import Producer

def produce_to_kafka():
    conf = {
        "bootstrap.servers": "broker:19092",
        "group.id": "airflow-producer"
    }

    producer = Producer(conf)

    producer.produce('task-submissions', "Message")
    producer.flush()

with DAG('kafka_producer') as dag:
    produce = PythonOperator(task_id='produce', python_callable=produce_to_kafka)
    produce