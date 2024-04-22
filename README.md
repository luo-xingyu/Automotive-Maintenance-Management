# Automotive-Maintenance-Management
Shanghai University Database principles (2) Project:

A B/S-based automobile maintenance management system developed based on the domestic database **OpenGauss**.

## Project Configuration
Environment: 
- OS : Ubuntu 23.10
- Python : 3.12.2
- Django : 3.2

### Install Docker In Your Linux
Since OpenGauss does not support Ubuntu, we chose to run it in Docker. For the installation of Docker, please refer to [Install Docker](https://blog.csdn.net/haobabiu/article/details/132892144).

Or you can enter the following command to install Docker directly.

**Old version**:
    
    sudo spt install docker.io

**New version (*Recommended*)**:

    curl -sSL https://get.docker.com/ | sh

### Pull Image Of OpenGauss
Pull the image through the following command:

    sudo docker pull enmotech/opengauss

### Create Docker 
Create a container to store data persistently and map ports to provide external access.


Check docker status:

    sudo docker ps

At this point, the image in the container is configured.

### Connect To Database In Django project
This step can be referred to [Connect OpenGauss](https://blog.csdn.net/weixin_45816954/article/details/121258831).


## Run Project
Enter the following command in the terminal:

    python manage.py runserver
