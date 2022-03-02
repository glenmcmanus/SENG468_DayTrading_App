#Copied from https://www.docker.com/blog/containerized-python-development-part-1/

# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /usr/transaction

# copy the dependencies file to the working directory
#COPY requirements.txt .

# install dependencies
RUN pip install pymongo

# copy the content of the local src directory to the working directory

RUN mkdir -p .
RUN mkdir -p ./Common
RUN mkdir -p ./TransactionServer

COPY ./../Common ./Common
COPY ./TransactionServer ./TransactionServer

# command to run on container start
CMD [ "python", "-m", "TransactionServer.src.transactionServer" ]