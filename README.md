# Express FE with Flask BE

This repository contains a demo of how would it look to have an application that:

- Serves pages from a FE microservice with a Node-Express server.
  - The pages could use SSR to render React Components.
- Has another microservice for the BE which uses Flask.
  - This BE would be used for all the operations that are not related to rendering pages.
- The FE microservice will use HTTP calls to the BE service when needed.

This approach simplifies a migration from Flask Jinja templates to SSR React Components,
without having to migrate the full application.

## How to use this Demo locally

### Requirements

To run this in an isolated/prod-like environment, install [Multipass](https://canonical.com/multipass).
Inside a Multipass VM you'll be able to run MicroK8s and Juju to simulate a real Production deployment.

To run the project in your own machine for development purposes you'll need:

- node
- npm
- docker
- docker-compose
- python3

### Dev environment

To start working get in the root project directory and run:

```bash
docker compose up --watch
```

Instead of bind mounts, this project uses compose watch to enable HMR.
For more info check the [Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/)
documentation.

### Debugging

If you need to get extra logs you have to add the following environment variable in front of
the command that you execute in _package.json_ (usually 'dev').

```bash
# The following enables all logs from express and vite
DEBUG=express:*,vite:*
# DEBUG=* enables all logs
```

To be able to attach a debugger to the running express application modify the _express-app/Dockerfile_
CMD line so that the last parameter is **dev:debug**.

## How to try it on Juju

All the scripts have been tested with bash, so if your main shell is not bash you'll
have to run them with:

```sh
bash scripts/<script-name>
```
