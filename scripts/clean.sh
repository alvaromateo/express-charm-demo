#!/usr/bin/env bash

function usage {
  echo "USAGE: clean.sh"
  echo "This script must be run from the project root (./scripts/clean.sh)"
}

project_root_regex="express-charm-demo/?$"

if [[ ! $(pwd) =~ ${project_root_regex} ]]; then
  usage
  exit 1
fi

export ROCKCRAFT_ENABLE_EXPERIMENTAL_EXTENSIONS=True
export CHARMCRAFT_ENABLE_EXPERIMENTAL_EXTENSIONS=True

cd express-app && rockcraft clean && cd ..
cd flask-app && rockcraft clean && cd ..

rm express-app/*.rock
rm express-app/charm/*.charm

rm flask-app/*.rock
rm flask-app/charm/*.charm
