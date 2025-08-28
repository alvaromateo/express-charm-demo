# Deploy and configure nginx-ingress-integrator
juju deploy nginx-ingress-integrator --trust
juju config nginx-ingress-integrator \
  service-hostname=express-app.local \
  service-name=express-app \
  service-port=8080 \
  service-namespace=express-flask \
  path-routes=/

# Set relation between nginx-ingress-integrator and express-app
juju relate express-app nginx-ingress-integrator:ingress

# Set relation between express-app and flask-app
juju relate express-app flask-app
