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
This way there's no conflict between virtual environments in the host and the containers.
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

### Requirements

To run this in an isolated/prod-like environment, install [Multipass](https://canonical.com/multipass).
Inside a Multipass VM you'll be able to run MicroK8s and Juju to simulate a real Production deployment.

There are scripts inside the _scripts/_ folder to install all the requirements inside the VM, so the
only requirement is Multipass (or some other VM).

### Run it

All the scripts have been tested with bash, so if your main shell is not bash you'll
have to run them with:

```sh
bash scripts/<script-name>
```

First of all you need to start a Multipass VM and you should set up a mounted directory so you can
access this project inside the VM. You can do so with the following commands:

```sh
multipass launch --cpus 4 --disk 50G --memory 4G --name charm-dev 24.04
multipass mount --type=classic charm-dev . express-charm-demo
```

Once the machine is running you can SSH into it:

```sh
multipass list
# once charm-dev is in running state
multipass shell charm-dev
```

Next you should set up the environment to be able to deploy the application.

```sh
cd express-charm-demo/scripts
./charmDev.sh
./deployApp.sh
```

And finally, if you modify anything in your application and want to deploy the
newest changes, there is also a script for that:

```sh
cd express-charm-demo/scripts
./refreshApp.sh
```

To access through your browser the K8s environment running inside the VM you'll
need to do

### Tips and troubleshooting

#### Requests not reaching express-app

If nginx-ingress-integrator seems like is not receiving the requests and forwarding them to the
FE application try to scale it down to 0 and back up to 1.

```sh
juju scale-application nginx-ingress-integrator 0
watch -n 2 -c juju status
# once application is stable
juju scale-application nginx-ingress-integrator 1
```

#### Virtual environments & node_modules

If you have some Python virtual environment created with python or node_modules installed,
delete them before running the Multipass VM and start everything inside it.

If you want to keep the Python virtual environments, be sure to name them something different
than _.venv_ (i.e. .venv_host). This way there will be no conflicts.

#### No keyring found

If you see this output when running some of the commands in the Multipass VM then do:

```sh
snapcraft export-login ~/snapcraft-login
export SNAPCRAFT_STORE_CREDENTIALS=$(cat ~/snapcraft-login)
charmcraft login --export ~/charmcraft-login
export CHARMCRAFT_AUTH=$(cat ~/charmcraft-login)
```
