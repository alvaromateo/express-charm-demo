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

rm express-app/*.rock
rm express-app/charm/*.charm

rm flask-app/*.rock
rm flask-app/charm/*.charm
