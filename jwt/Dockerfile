FROM python:buster
WORKDIR /code
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  gcc
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python", "serverZMQ.py","main", "5555", "5556", "5557", "5558", "keyServer/server.key_secret", "keyClient/client.key", "keyClient/client.key", "usr", "rsc", "testmdp"]
