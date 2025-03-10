FROM node:20-alpine3.17
LABEL maintainer="Clarence Advincula Baluyot <akingprincess@gmail.com> https://www.linkedin.com/in/clarencebaluyot/"
# create destination directory
RUN mkdir -p /app
WORKDIR /app

# update and install dependency
RUN apk update && apk upgrade
RUN apk add git

# copy the app, note .dockerignore
COPY . /app/
RUN npm install
# RUN npm run build

EXPOSE 3000
EXPOSE 80

# CMD [ "npm", "start" ]
