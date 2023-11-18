FROM amazon/aws-lambda-python:3.8

EXPOSE 8080
CMD [ "flaskapp.handler" ]

RUN pip install pyuwsgi
COPY requirements.txt /tmp/

# Set environment variables for TypeDB version and download URL
ENV TYPEDB_VERSION=2.19.1
ENV TYPEDB_DOWNLOAD_URL=https://github.com/vaticle/typedb/releases/download/${TYPEDB_VERSION}/typedb-all-linux-${TYPEDB_VERSION}.tar.gz

# Install needed utilities, download, extract and set up TypeDB
RUN yum install -y wget tar gzip && \
    mkdir -p /opt/typedb && \
    wget -O /tmp/typedb.tar.gz $TYPEDB_DOWNLOAD_URL && \
    tar -xzf /tmp/typedb.tar.gz -C /opt/typedb --strip-components=1 && \
    ln -s /opt/typedb/typedb /usr/local/bin/typedb && \
    rm /tmp/typedb.tar.gz && \
    yum clean all

# Specify the command to run when the container starts
CMD ["typedb", "server"]

RUN yum makecache && \
    yum -y install Cython && \
    yum -y install gcc && \
    pip install -r /tmp/requirements.txt && \
    yum -y remove gcc && \
    yum clean all && \
    rm -rf /var/cache/yum datasets

COPY requirements.setup.txt /tmp/
RUN pip install --upgrade -r /tmp/requirements.setup.txt

RUN python3 -m spacy download en_core_web_lg
RUN python3 -m pip install --upgrade pymupdf
