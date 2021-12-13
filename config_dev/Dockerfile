FROM python:3.7-slim

RUN apt-get update && apt-get install -y netcat && apt-get install dos2unix

# User arguments on Dockerfile build - declared in the Docker-Compose file
ARG SETTINGS
ARG PORT

# Set working directory
WORKDIR /opt/i2amparis


# Install Project requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

#Copy whole project
COPY . .

EXPOSE ${PORT}
RUN dos2unix config_dev/run.sh
CMD bash config_dev/run.sh
