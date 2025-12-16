#!/usr/bin/env bash

function usage {
  echo "USAGE: setupCOS.sh"
  echo "This script must be run from the project root (./scripts/setupCOS.sh)"
}

project_root_regex="express-charm-demo/?$"

if [[ ! $(pwd) =~ ${project_root_regex} ]]; then
  usage
  exit 1
fi

source scripts/commonVars.sh

current_model=$(juju switch | sed 's/.*\/(.*)/\1/')

# Set model if needed
juju_model=$(juju models --format yaml | yq '.models.[] | select(."short-name" == "cos") | ."short-name"')
if [ -z ${juju_model} ]; then
  # TODO: check if mk8s cloud exists and add it if it doesn't
  echo "Adding COS model..."
  juju add-model cos mk8s
  juju switch cos
  juju set-model-constraints -m cos arch=${architecture}
fi

# TODO: add checks to make sure we don't re-deploy COS
juju switch cos
juju deploy cos-lite --trust

# Switch back to the previous model to leave everything as it was
juju switch ${current_model}
