# Install the base requirements for the app.
# This stage is to support development.
FROM python:3.8-slim-buster AS base
WORKDIR /home
COPY ./requirements.txt /home/requirements.txt

RUN apt-get update && apt-get install -y wget libsasl2-2 \
		libsasl2-dev python3-dev

RUN pip3 install -r requirements.txt

ADD ./app /home/app
ADD ./gdelt_code /home/gdelt_code
ADD ./README.md /home/README.md

# ENTRYPOINT ["python3", "gdelt_code/main.py"]
