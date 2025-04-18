# TECHNICAL TASK
This is an example of a Django project which is running using Docker.


## Technologies
* Docker 
* Docker Compose


# Project settings
1. Clone this project's repository to your local machine using SSH
```bash
  git clone git@github.com:akostanda/FirstDjangoProject.git
```
2. Move to it
```bash
  cd <your project name>
```


## Docker Linux Installation
1. Use documentation: [Docker documentation for Linux](https://docs.docker.com/engine/install/)
2. Check if Docker is installed successfully
```bash
  sudo docker --version
```
You should see output with the Docker version, for example: Docker version 28.1.1, build 4eba377
2. Check if Docker Compose is installed successfully
```bash
  sudo docker-compose --version
```
You should see output with the Docker Compose version, for example: docker-compose version 1.29.2, build 5eba378


To run the program after downloading, follow these steps:
1. Install the necessary dependencies:
```bash
  sudo docker-compose up --build
```
2. Project run
```bash
  sudo docker-compose up
```
3. Quit Docker running with CONTROL-C:


## Endpoints
Open API_Documentation.yaml to see all endpoints.


## Addition information
Now for testing purpose, notification email after user registration and registration to an event
are sent to the console. If you want to send a real email, you should change EMAIL_HOST_USER and
EMAIL_HOST_PASSWORD parameters with your real Google email address and password for a Google app.
Also, you should uncomment lines 155–165 and comment line 152 in settings.py