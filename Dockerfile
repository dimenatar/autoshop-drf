FROM python:3.12-slim

RUN apt-get update && apt-get install -y netcat && apt-get clean

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

RUN groupadd -r myuser && useradd -r -g myuser myuser
RUN chown -R myuser:myuser /app
USER myuser


COPY requirements.txt .
COPY .env .
COPY entry_point.sh /entry_point.sh
COPY . /usr/src/app/

RUN pip install python-dotenv
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/entry_point.sh"]

#docker ignore
#docker user
# layers
# копирование на несколько этапов; 1 -> requirements, отдельно .env
# вынести entry_point.sh проверку инициализацию бд