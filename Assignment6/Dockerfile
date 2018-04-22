
FROM ubuntu:latest
MAINTAINER Rajdeep Dua "dua_rajdeep@yahoo.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]

# FROM python:3.6
# MAINTAINER Kai Lukowiak "kailukowiak@gmail.com"
# ADD . /code
# WORKDIR /code
# RUN pip install -r requirements.txt
# EXPOSE  5000
# CMD python app.py


