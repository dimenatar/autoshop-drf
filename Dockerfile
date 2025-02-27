FROM python:3.12-slim



RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

#RUN groupadd -r myuser && useradd -r -g myuser myuser
#RUN mkdir -p /home/myuser/.cache/pip && chown -R myuser:myuser /home/myuser
#RUN chown -R myuser:myuser /usr/src/app/



RUN apt-get update && apt-get install -y netcat-traditional && apt-get clean

RUN useradd -m -r myuser && \
   mkdir /app && \
   chown -R myuser /usr/src/app/

WORKDIR /usr/src/app/

#RUN useradd --create-home --shell /bin/bash myuser
USER myuser
#WORKDIR /home/myuser

COPY requirements.txt .
COPY .env .
COPY entry_point.sh /entry_point.sh
COPY . /usr/src/app/



RUN pip install python-dotenv
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/entry_point.sh"]