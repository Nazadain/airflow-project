from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.models.param import Param

from sensors.kafka_sensor import KafkaMessageSensor


def preparationTask(**context):
    # [обновление запроса в Redis]
    # создание папки в stud
    # получение данных и их сохранение

    print("Hello world!")

@task(task_id = 'SuccessfulEnding', trigger_rule = TriggerRule.ALL_SUCCESS, retries = 0)
def success():
    print("ALL_SUCCESS")

@task(task_id = 'FailedEnding', trigger_rule = TriggerRule.ONE_FAILED, retries = 0)
def fail():
    print("ONE_FAILED")


with DAG('Teyusu_TestStudentCode',
         description = 'Teyusu | Test student code',
         default_args = {
             'depends_on_past': False,
             'retries': 0
         },
         schedule_interval = None,
         params = {
             'uuid': Param("", type = 'string'),
             'exno': Param(0, type = 'integer', minimum = 0)
         }) as dag:

    WaitMessageTask = KafkaMessageSensor(
        task_id="WaitMessageTask",
        topic="task-submissions",
        kafka_server="broker:19092",
    )

    PreparationTask = PythonOperator(
        task_id = 'Preparation',
        retries = 0,
        python_callable = preparationTask)
    CompilationTask = BashOperator(
        task_id = 'Compilation',
        retries = 0,
        bash_command = 'docker exec airflow-project-gcc-1 /teyusu/Compile.sh {{ dag_run.conf["uuid"] }} {{ dag_run.conf["exno"] }}')
    TestingTask = BashOperator(
        task_id = 'Testing',
        retries = 0,
        bash_command = '/teyusu/Test.sh {{ dag_run.conf["uuid"] }}')

    WaitMessageTask >> PreparationTask >> CompilationTask >> TestingTask

    dagtsk = list(dag.tasks)
    dagtsk >> success()
    dagtsk >> fail()