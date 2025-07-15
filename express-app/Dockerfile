# syntax=docker/dockerfile:1
FROM node:lts-alpine
RUN addgroup -S app && adduser -S app -G app
USER app

WORKDIR /code

COPY --chown=app:app package.json package-lock.json ./
RUN npm install

EXPOSE 3000
EXPOSE 9229
COPY --chown=app:app . ./

# TODO: add possibility to attach debugger

CMD ["npm", "run", "dev"]
