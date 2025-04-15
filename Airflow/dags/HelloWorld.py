from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

def helloWorld():
    print("Hello world!")

with DAG('Teyusu_HelloWorld',
         description = 'Teyusu | A simple test DAG',
         default_args = {
             'depends_on_past': False,
             'retries': 0
         },
         schedule_interval = None) as dag:
    t1 = DummyOperator(task_id = 'Dummy')
    t2 = BashOperator(task_id = 'Sleeping', bash_command = 'sleep 5'),
    t3 = PythonOperator(task_id = 'Hello', python_callable = helloWorld)

    t1 >> t2 >> t3