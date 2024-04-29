# syntax=docker/dockerfile:1
FROM python:3.8
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
COPY start_services.sh /app
RUN chmod +x /app/start_services.sh
CMD ["./start_services.sh"]
