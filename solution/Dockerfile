FROM python:3.12.1-alpine3.19

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV SERVER_PORT=8080

RUN chmod +x ./start.sh

ENTRYPOINT ["./start.sh"]