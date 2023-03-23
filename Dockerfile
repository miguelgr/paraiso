FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes \
    git

COPY requirements-dev.txt requirements-dev.txt
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY paraiso /app/paraiso

COPY manage.py /app/
COPY entrypoint.sh /app/

EXPOSE 8000

CMD ["bash", "entrypoint.sh"]
