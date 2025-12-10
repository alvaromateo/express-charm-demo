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


# Create rock
rockcraft pack
rockcraft.skopeo copy \
  --insecure-policy \
  --dest-tls-verify=false \
  oci-archive:${rock_name}_${version}_${architecture}.rock \
  docker://localhost:32000/${rock_name}:${version}

# Create charm
cd charm
charmcraft fetch-libs
charmcraft pack
