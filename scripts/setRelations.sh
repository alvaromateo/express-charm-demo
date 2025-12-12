# Deploy and configure nginx-ingress-integrator
juju deploy nginx-ingress-integrator --trust
juju config nginx-ingress-integrator \
  service-hostname=demo-app.local \
  service-name=demo-app \
  service-port=3010 \
  service-namespace=express-flask \
  path-routes=/ \
  rewrite-enabled=false \
  rewrite-target=/

# Set relation between nginx-ingress-integrator and demo-app
juju relate demo-app:ingress-frontend nginx-ingress-integrator:ingress
