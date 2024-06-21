# airflow_training
## Remote to Server
Remote to VM by Secure Shell (SSH) protocol. <br />
<br />
```
ssh {user}@{host}
```
Change ```{user}``` to your user and ```{host}``` to your external IP of VM. <br />
After run command. There are 2 promts in terminal.<br />
- Trust this connection. Type ```yes```.<br />
- Authen your user.Type your password.<br />

If connection success.You will be logged into the remote server, and you'll see the remote system's command prompt.<br />

## Creat Airflow project directory
### Initializing Environment
Before starting Airflow for the first time, you need to prepare your environment, i.e. create the necessary files, directories and initialize the database.<br />
Change your current directory to root directory and create ```airflow``` folder.<br />
```
cd /
sudo mkdir airflow
# change {user} to your user
sudo chown {user}:{user} airflow
```
Access airflow folder and create necessory directory for airflow consist of <br />
- dags
- logs
- plugins
- config

```
cd /airflow
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
### Initialize the database
Before initialize database.You should create ```docker-compose.yml``` which is a configuration file used by Docker Compose, a tool for defining and running multi-container Docker applications. <br /><br />
Create ```docker-compose.yml``` and edit by add code from [docker-compose.yml](https://github.com/phawatmk/airflow_training/blob/main/docker-compose.yml) to ```docker-compose.yml``` file.<br /><br />
On all operating systems, you need to run database migrations and create the first user account. To do this, run.

```
sudo docker compose up airflow-init
```

After initialization is complete, you should see a message like this:

```
airflow-init_1       | Upgrades done
airflow-init_1       | Admin user airflow created
airflow-init_1       | 2.9.2
start_airflow-init_1 exited with code 0
```
### Running Airflow
After initialize database.You can start running airflow by run this command.<br />
```
sudo docker compose up -d
```

You can check the condition of the containers and make sure that no containers are in an unhealthy condition.<br />
```
sudo docker ps
```
![alt text](https://github.com/phawatmk/airflow_training/blob/main/images/docker_ps.png) <br />

### Create DAG
DAG is a collection of all the tasks you want to run, organized in a way that reflects their relationships and dependencies. A DAG is defined in a Python script, which represents the DAGs structure (tasks and their dependencies) as code.<br />
DAG have to be created in dags folder.<br />
Change directory to dags folder<br />
```
cd dags
```
1. Create python file name ```{user}_dag.py``` and replace ```{user}``` to your user.<br /><br />
2. Edit file by vi or nano by add code from [phawatmk_dag.py](https://github.com/phawatmk/airflow_training/blob/main/phawatmk_dag.py).<br /><br />
3. Revised line 10 change ```<YOUR DAG NAME>``` to ```{user}_dag``` (replace ```{user}``` to your user).<br /><br />
4. Save file.<br /><br />

After save file.DAG will be shown in web interface.<br /><br />

### Accessing the web interface
Once the cluster has started up, you can log in to the web interface and begin experimenting with DAGs.<br />
The webserver is available at: ```http://{YOUR HOST}:8080```. The default account has the login ```airflow``` and the password ```airflow```.<br />
![alt text](https://github.com/phawatmk/airflow_training/blob/main/images/airflow_login.png) <br />

### Running DAG
If your DAG was correct.It will be shown in web interface.Now you can running your DAG.<br />
![alt text](https://github.com/phawatmk/airflow_training/blob/main/images/airflow_ui.png) <br />
Click on your DAG.<br />
You can run DAG by click on run bottom and click triggering DAG.<br />
When DAG finish running. You can see log in Logs tab bar and checking task run and each log.<br />
![alt text](https://github.com/phawatmk/airflow_training/blob/main/images/airflow_logs.png) <br />

You can check data which's loaded into postgresql by exec to docker image by run this command.<br />

```
sudo docker exec -it airflow-postgres-1 /bin/bash
```
and run this command below to access postgresql.<br />
```
psql -d postgres -U airflow
```
Now you can check result by query table ```public.customer_detail```
```
select * from public.customer_detail;
```
You will get result like below:
![alt text](https://github.com/phawatmk/airflow_training/blob/main/images/result.png) <br />
### Add new task
Edit your DAG file. 
- add this code below to line 80.<br />
```
@task
def save_data_to_file():

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
    
    # Define your SQL query
    query = 'SELECT job, city, avg(salary) as average_salary FROM public.customer_detail'

    # Use pandas to execute the query and load the data into a DataFrame
    df = pd.read_sql_query(query, engine)

    # Save the DataFrame to a CSV file
    df.to_csv('/opt/airflow/plugins/average_salary.csv', index=False)
```
 - add this code below to line 122
```
save_data_to_file_task = save_data_to_file()
```
- edit last as this code below
```
generate_df_task >> load_df_to_db_task >> save_data_to_file_task
```
Then save file and open DAG in web interfaces.<br />

