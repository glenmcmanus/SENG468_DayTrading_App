#Copied from https://www.docker.com/blog/containerized-python-development-part-1/

# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /usr/legacy_quote

# copy the dependencies file to the working directory
#COPY requirements.txt .

# install dependencies
#RUN pip install -r requirements.txt
RUN pip install redis
RUN apt-get update && apt-get -y dist-upgrade
RUN apt install -y netcat

# copy the content of the local src directory to the working directory

RUN mkdir -p .
RUN mkdir -p ./Common
RUN mkdir -p ./LegacyServer

COPY ./Common ./Common
COPY ./LegacyServer ./LegacyServer

# command to run on container start
CMD [ "python", "-m", "LegacyServer.src.queryLegacyServer.py" ]