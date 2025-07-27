FROM python:3.13.5-alpine3.21

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "sh", "entrypoint.sh" ]