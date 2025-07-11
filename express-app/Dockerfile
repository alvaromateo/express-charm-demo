# syntax=docker/dockerfile:1
FROM node:lts-alpine
WORKDIR /code
COPY . .
RUN npm install
RUN npm run build
CMD ["node", "./src/index.js"]