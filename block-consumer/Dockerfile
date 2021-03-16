FROM python:3.8-slim
WORKDIR .

COPY requirements.txt .
RUN apt update && apt -y install postgresql libpq-dev gcc
RUN pip3 install --no-cache-dir -r requirements.txt

COPY main.py .

CMD [ "python3", "./main.py"]