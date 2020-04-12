FROM mongo:latest
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
# install Python 3
RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get -y install python3.7-dev
WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
COPY . .
CMD ["flask", "run"]
