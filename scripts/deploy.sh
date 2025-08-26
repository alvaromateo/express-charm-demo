#!/usr/bin/env bash

function usage {
  echo "USAGE: deploy.sh"
  echo "This script must be run from the project root (./scripts/deploy.sh)"
}

project_root_regex="express-charm-demo/?$"

if [[ ! $(pwd) =~ ${project_root_regex} ]]; then
  usage
  exit 1
fi

source scripts/commonVars.sh

# Set model if needed
juju_model=$(juju models --format yaml | yq '.models.[] | select(."short-name" == "express-flask") | ."short-name"')
if [ -z ${juju_model} ]; then
  echo "Adding new model..."
  KUBECONFIG=~/microk8s.yaml juju add-k8s mk8s --client
  KUBECONFIG=~/microk8s.yaml juju add-k8s mk8s --controller dev
  juju add-model express-flask mk8s
  juju switch express-flask
  juju set-model-constraints -m express-flask arch=${architecture}
fi

# Check if apps are already deployed
express_app_deployed=`juju status --format yaml \
  | yq --arg CHARM_NAME ${express_charm_name} \
    '.applications.[] | select(."charm-name" == $CHARM_NAME) | ."charm-name"' \
  | wc -l`
flask_app_deployed=`juju status --format yaml \
  | yq --arg CHARM_NAME ${flask_charm_name} \
    '.applications.[] | select(."charm-name" == $CHARM_NAME) | ."charm-name"' \
  | wc -l`

# Deploy or refresh applications
if [ $express_app_deployed -eq 1 ]; then
  # app is already deployed, so we refresh it
  juju refresh ${express_charm_name} \
    --path ./express-app/charm/${express_charm_name}_${architecture}.charm \
    --resource app-image=localhost:32000/${express_rock_name}:${version_express}
else
  # app is not deployed
  juju deploy \
    ./express-app/charm/${express_charm_name}_${architecture}.charm \
    ${express_charm_name} \
    --resource app-image=localhost:32000/${express_rock_name}:${version_express}
fi

if [ $flask_app_deployed -eq 1 ]; then
  # app is already deployed, so we refresh it
  juju refresh ${flask_charm_name} \
    --path ./flask-app/charm/${flask_charm_name}_${architecture}.charm \
    --resource flask-app-image=localhost:32000/${flask_rock_name}:${version_flask}
else
  # app is not deployed
  juju deploy \
    ./flask-app/charm/${flask_charm_name}_${architecture}.charm \
    ${flask_charm_name} \
    --resource flask-app-image=localhost:32000/${flask_rock_name}:${version_flask}
fi
