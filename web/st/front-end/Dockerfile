FROM node:12.2.0-alpine

COPY . /web/

# set working directory
WORKDIR /web/st

# add `/app/node_modules/.bin` to $PATH
ENV PATH /node_modules/.bin:$PATH

# install and cache app dependencies
RUN npm install --silent
RUN npm install react-scripts@3.0.1 -g --silent

# start app
EXPOSE 3000