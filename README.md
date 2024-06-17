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
