FROM python:3.12-slim
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
RUN apt-get update && apt-get install -y netcat-traditional && apt-get clean
RUN pip install --no-cache-dir python-dotenv
RUN useradd -m -r myuser && \
   mkdir /app && \
   chown -R myuser /usr/src/app/
WORKDIR /usr/src/app/
USER myuser

COPY requirements.txt .
COPY .env /.env
COPY entry_point.sh /entry_point.sh
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["/entry_point.sh"]