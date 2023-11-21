# Use an official Python 3.11 runtime as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install uwsgi, commonly used for serving Python applications
RUN pip install pyuwsgi

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Adding a different user
# RUN adduser --disabled-password --gecos '' myuser
# USER myuser

# Copy the rest of your application's code into the container at /app
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Command to run your application
# CMD ["pyuwsgi", "--http", "0.0.0.0:8080", "--module", "gis-analytics:app"]
CMD ["uwsgi", "--http", "0.0.0.0:8080", "--wsgi-file", "gis-analytics.py", "--callable", "app", "--uid", "1000", "--gid", "2000", "--master", "--enable-threads"]

# Alternatively, if you want to run tests instead of starting the Flask app, use this CMD:
# CMD ["pytest", "tests/"]






# Install needed utilities, download, extract and set up TypeDB
# RUN yum install -y wget tar gzip && \
#     mkdir -p /opt/typedb && \
#     wget -O /tmp/typedb.tar.gz $TYPEDB_DOWNLOAD_URL && \
#     tar -xzf /tmp/typedb.tar.gz -C /opt/typedb --strip-components=1 && \
#     ln -s /opt/typedb/typedb /usr/local/bin/typedb && \
#     rm /tmp/typedb.tar.gz && \
#     yum clean all

# # Specify the command to run when the container starts
# CMD ["typedb", "server"]

# RUN yum makecache && \
#     yum -y install Cython && \
#     yum -y install gcc && \
#     pip install -r /tmp/requirements.txt && \
#     yum -y remove gcc && \
#     yum clean all && \
#     rm -rf /var/cache/yum datasets

# COPY requirements.setup.txt /tmp/
# RUN pip install --upgrade -r /tmp/requirements.setup.txt

# RUN python3 -m spacy download en_core_web_lg
# RUN python3 -m pip install --upgrade pymupdf
