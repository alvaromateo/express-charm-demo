#!/usr/bin/env bash

function usage {
  echo "USAGE: deployApp.sh"
  echo "This script must be run from the project root (./scripts/commonVars.sh)"
}

project_root_regex="express-charm-demo/?$"

if [[ ! $(pwd) =~ ${project_root_regex} ]]; then
  usage
  exit 1
fi

# Variables
version=""
rock_name=""
charm_name=""

# dpkg is not available on macOS, so if the first command fails it means we're on macOS
# and the "uname -m" command is run, which outputs "arm64"
architecture=$(dpkg --print-architecture || uname -m)

version=$(grep '^version:' 'rockcraft.yaml' | cut -d' ' -f2 | tr -d '"')
rock_name=$(grep '^name:' 'rockcraft.yaml' | cut -d' ' -f2)
cd charm
charm_name=$(grep '^name:' 'charmcraft.yaml' | cut -d' ' -f2)
cd ..
