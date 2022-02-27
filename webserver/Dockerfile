FROM node:16

WORKDIR /usr/webserver/

RUN mkdir -p ./api

COPY ./api/package*.json ./api/.

WORKDIR /usr/webserver/api/
RUN npm install

WORKDIR /usr/webserver/

COPY . .

EXPOSE ${WEB_PORT_EXT}

WORKDIR /usr/webserver/api

#RUN npm start
CMD ["npm", "start"]