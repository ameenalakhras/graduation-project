# graduation-project

This project is the graduation project for the year 2020, its goal is to create a virtual classroom for the teachers and the students to communicate and make assinments and other activities at alazhar university - Gaza - Palestine.

## Browsing the project
1. currently all the work done (code changes) are on **heroku_dev branch** and it's applied every couple of changes to **heroku_deploy branch**.
2. the **master branch** has the **docker container** for the project to run on any device, The **master branch** is only updated when the is big milestones done to the **heroku_deploy branch**.

## The project structure
BackEnd: Django REST
FrontEnd: React
DataBase: PostgreSQL

### runing the docker on the master branch
( it will take some time to download the dependencies depending on your internet connection)
1. make sure you have [docker](https://www.docker.com/) installed
2. run the next command:
```
$sudo docker-compose up --build
```
