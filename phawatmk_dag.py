from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
from airflow.models import Variable
import pendulum
import pandas as pd
from faker import Faker
from sqlalchemy import create_engine

dag_id = '<YOUR DAG NAME>'

@task
def generate_dataframe():
    # Initialize Faker
    fake = Faker()

    # Generate sample data
    data = {
        'id': [i for i in range(1, 1001)],
        'name': [fake.name() for _ in range(1000)],
        'age': [fake.random_int(min=18, max=70) for _ in range(1000)],
        'job' : [fake.job() for _ in range(1000)],
        'city': [fake.city() for _ in range(1000)],
        'salary': [fake.random_int(min=30000, max=100000) for _ in range(1000)]
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame
    return df


@task
def load_df_to_db(df):

    host = 'postgres'
    port = '5432'
    database_name = 'postgres'
    schema_name = 'public'
    username = 'airflow'
    password = 'airflow'
    connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database_name}'
    table_name = 'customer_detail'
    
    # Create a SQLAlchemy engine
    engine = create_engine(connection_string)
    conn = engine.connect()

    # drop table
    conn.execute(f'DROP TABLE IF EXISTS public.{table_name}')

    # create table
    conn.execute(f'''
        CREATE TABLE IF NOT EXISTS public.{table_name}
        (
            id varchar,
            name varchar,
            age integer,
            job varchar,
            city varchar,
            salary integer
        )
        ''')

    # Insert data
    if len(df) > 0:

        try:
            # Load the DataFrame into PostgreSQL using df.to_sql
            df.to_sql(name=table_name, schema=schema_name, con=conn, if_exists='replace', index=False)
            conn.close()
            print('Load data success!!')
        
        except Exception as e:
            raise e
    else:
        print('no data')

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

with DAG(dag_id=dag_id,
  schedule_interval=None,
  default_args=default_args,
  schedule=None,
  start_date=pendulum.datetime(2024, 1, 10, tz="Asia/Bangkok"),
  catchup=False
  ) as dag:
  

    generate_df_task = generate_dataframe()
    load_df_to_db_task = load_df_to_db(generate_df_task)


    generate_df_task >> load_df_to_db_task >> send_end_email