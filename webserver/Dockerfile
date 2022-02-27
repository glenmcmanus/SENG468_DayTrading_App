FROM node:16

WORKDIR /usr/src/

COPY ./app/package*.json ./app/.

WORKDIR /usr/src/app
RUN npm install

WORKDIR /usr/src/

COPY . .

EXPOSE ${WEB_PORT_EXT}

WORKDIR /usr/src/app
CMD [ "npm", "start" ]