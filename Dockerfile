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

# To run Jupyter-Notebook
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]

# Get Java to run Spark
#ENV JAVA_HOME=/opt/openjdk-11
#ENV PATH=$JAVA_HOME/bin:$PATH

RUN wget -O /openjdk.tgz https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz
RUN echo "99be79935354f5c0df1ad293620ea36d13f48ec3ea870c838f20c504c9668b57 */openjdk.tgz" | sha256sum -c
RUN mkdir -p "/opt/openjdk-11"
RUN tar --extract --file /openjdk.tgz --directory "/opt/openjdk-11" --strip-components 1
RUN rm /openjdk.tgz


# ENTRYPOINT ["python3", "gdelt_code/main.py"]
