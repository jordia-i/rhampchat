  
FROM python:3.9.1-slim

RUN mkdir /opt/webhook
WORKDIR /opt/webhook

ADD requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .
ADD . .

EXPOSE 5000
ENV FLASK_APP=webhookreceiver.py

CMD python3 webhookregister.py && flask run --host 0.0.0.0 --port 5000