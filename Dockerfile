FROM python:3.13.5-alpine3.21

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . . 

RUN pip3 install -r requirements.txt

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "sh", "entrypoint.sh" ]