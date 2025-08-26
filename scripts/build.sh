#!/usr/bin/env bash

function usage {
  echo "USAGE: build.sh"
  echo "This script must be run from the project root (./scripts/build.sh)"
}

project_root_regex="express-charm-demo/?$"

if [[ ! $(pwd) =~ ${project_root_regex} ]]; then
  usage
  exit 1
fi

source scripts/commonVars.sh

export ROCKCRAFT_ENABLE_EXPERIMENTAL_EXTENSIONS=True
export CHARMCRAFT_ENABLE_EXPERIMENTAL_EXTENSIONS=True


# Create express-app rock
cd express-app
rockcraft pack
rockcraft.skopeo copy \
  --insecure-policy \
  --dest-tls-verify=false \
  oci-archive:${express_rock_name}_${version_express}_${architecture}.rock \
  docker://localhost:32000/${express_rock_name}:${version_express}
cd ..

# Create flask-app rock
cd flask-app
rockcraft pack
rockcraft.skopeo copy \
  --insecure-policy \
  --dest-tls-verify=false \
  oci-archive:${flask_rock_name}_${version_flask}_${architecture}.rock \
  docker://localhost:32000/${flask_rock_name}:${version_flask}
cd ..

# Create express-app charm
cd express-app/charm
charmcraft fetch-libs
charmcraft pack
cd ../..

# Create flask-app charm
cd flask-app/charm
charmcraft fetch-libs
charmcraft pack
cd ../..
