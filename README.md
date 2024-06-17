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
chown {user}:{user} airflow
```
Access airflow folder and create necessory directory for airflow consist of <br />
- dags
- logs
- plugins
- config

```
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
### Initialize the database
Before initialize database.You should create ```docker-compose.yml``` which is a configuration file used by Docker Compose, a tool for defining and running multi-container Docker applications. <br />
create ```docker-compose.yml``` by vi or nano and edit by add this code to ```docker-compose.yml``` file.<br />
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
