# syntax=docker/dockerfile:1
FROM node:lts-alpine
RUN addgroup -S app && adduser -S app -G app
USER app

WORKDIR /code

COPY --chown=app:app package.json package-lock.json ./
RUN npm install

COPY --chown=app:app . ./

CMD ["npm", "run", "dev"]
