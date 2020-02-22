# graduation-project
# Version: 0.0.1
FROM python:3

# Project Files and Settings
ARG PROJECT=django
ARG PROJECT_DIR=/var/www/${PROJECT}
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
RUN cd $PROJECT_DIR
ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Server
EXPOSE 3000
EXPOSE 8000
STOPSIGNAL SIGINT
#CMD ["sleep", "infinity"]
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
