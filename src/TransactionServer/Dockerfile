#Copied from https://www.docker.com/blog/containerized-python-development-part-1/

# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
#COPY requirements.txt .

# install dependencies
#RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory

RUN mkdir -p ./src
RUN mkdir -p ./src/Common
RUN mkdir -p ./src/TransactionServer

COPY ./Common ./src/Common
COPY ./TransactionServer ./src/TransactionServer

# command to run on container start
CMD [ "python", "-m", "src.TransactionServer.transactionServer" ]