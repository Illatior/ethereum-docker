FROM python:3.8-slim-buster
WORKDIR .

COPY requirements.txt .

RUN apt update && \
    apt install -y gcc

RUN pip3 install  -r requirements.txt

COPY main.py .


CMD [ "python3", "-u", "./main.py"]