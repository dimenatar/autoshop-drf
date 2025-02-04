FROM python:3.12-slim

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip install python-dotenv
RUN pip install --no-cache-dir -r requirements.txt

#docker ignore
#docker user
# layers
# копирование на несколько этапов; 1 -> requirements, отдельно .env
# вынести entry_point.sh проверку инициализацию бд