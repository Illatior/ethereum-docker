FROM python:3.8-alpine
WORKDIR .

COPY requirements.txt .
COPY main.py .

RUN pip3 install --no-cache-dir -r requirements.txt


CMD [ "python3", "-u", "./main.py"]