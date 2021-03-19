FROM python:3.8-alpine
WORKDIR .

COPY requirements.txt .

RUN apk update && \
    apk add --virtual .build-deps gcc python3-dev musl-dev && \
    apk add postgresql-dev
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apk del .build-deps

COPY main.py .

CMD [ "python3", "-u", "./main.py"]