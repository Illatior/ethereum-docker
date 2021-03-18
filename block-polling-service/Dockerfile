FROM python:3.8-slim-buster
WORKDIR .

COPY requirements.txt .
COPY main.py .

RUN apt update && \
    apt install -y gcc

RUN pip3 install  -r requirements.txt


CMD [ "python3", "-u", "./main.py"]