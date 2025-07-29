#!/usr/bin/env bash

function usage {
  echo "USAGE: deployApp.sh"
  echo "This script must be run from the project root (./scripts/deployApp.sh)"
}

project_root_regex="express-charm-demo/?$"

if [[ ! $(pwd) =~ ${project_root_regex} ]]; then
    usage
    exit 1
fi

# Variables
version_express=""
version_flask=""
express_rock_name=""
flask_rock_name=""
express_charm_name=""
flask_charm_name=""

# dpkg is not available on macOS, so if the first command fails it means we're on macOS
# and the "uname -m" command is run, which outputs "arm64"
architecture=$(dpkg --print-architecture || uname -m)

export ROCKCRAFT_ENABLE_EXPERIMENTAL_EXTENSIONS=True
export CHARMCRAFT_ENABLE_EXPERIMENTAL_EXTENSIONS=True

# Set model if needed
juju_model=$(juju models --format yaml | yq '.models.[] | select(."short-name" == "express-flask") | ."short-name"')
if [ -z ${juju_model} ]; then
    echo "Adding new model..."
    juju add-model express-flask
    juju set-model-constraints -m express-flask arch=${architecture}
fi


# Create express-app rock
cd express-app
echo "Entering express-app"
version_express=$(grep '^version:' 'rockcraft.yaml' | cut -d' ' -f2 | tr -d '"')
express_rock_name=$(grep '^name:' 'rockcraft.yaml' | cut -d' ' -f2)
rockcraft pack
rockcraft.skopeo copy \
  --insecure-policy \
  --dest-tls-verify=false \
  oci-archive:${express_rock_name}_${version_express}_${architecture}.rock \
  docker://localhost:32000/${express_rock_name}:${version_express}
cd ..
echo "Left express-app"

# Create flask-app rock
cd flask-app
echo "Entering flask-app"
version_flask=$(grep '^version:' "rockcraft.yaml" | cut -d' ' -f2 | tr -d '"')
flask_rock_name=$(grep '^name:' 'rockcraft.yaml' | cut -d' ' -f2)
rockcraft pack
rockcraft.skopeo copy \
  --insecure-policy \
  --dest-tls-verify=false \
  oci-archive:${flask_rock_name}_${version_flask}_${architecture}.rock \
  docker://localhost:32000/${flask_rock_name}:${version_flask}
cd ..
echo "Left flask-app"

# Create express-app charm
cd express-app/charm
echo "Entering express-app/charm"
express_charm_name=$(grep '^name:' 'charmcraft.yaml' | cut -d' ' -f2)
charmcraft fetch-libs
charmcraft pack
cd ../..
echo "Left express-app/charm"

# Create flask-app charm
cd flask-app/charm
echo "Entering flask-app/charm"
flask_charm_name=$(grep '^name:' 'charmcraft.yaml' | cut -d' ' -f2)
charmcraft fetch-libs
charmcraft pack
cd ../..
echo "Left flask-app/charm"

# Deploy express-app
juju deploy \
  ./express-app/charm/${express_charm_name}_${architecture}.charm ${express_charm_name} \
  --resource app-image=localhost:32000/${express_rock_name}:${version_express}

# Deploy flask-app
juju deploy \
  ./flask-app/charm/${flask_charm_name}_${architecture}.charm ${flask_charm_name} \
  --resource flask-app-image=localhost:32000/${flask_rock_name}:${version_flask}

# Set relation between express-app and flask-app

# Deploy and configure nginx-ingress-integrator
