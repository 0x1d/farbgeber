FROM python:3.7

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "farbgeber_mqtt.py"]
