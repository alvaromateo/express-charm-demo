# syntax=docker.io/docker/dockerfile:1.7-labs
FROM node:lts-alpine
RUN addgroup -S app && adduser -S app -G app
USER app

WORKDIR /app

COPY --chown=app:app app/*.json ./
RUN npm install

COPY --exclude=app/node_modules --chown=app:app app ./

CMD ["npm", "run", "dev"]
