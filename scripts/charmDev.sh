#!/usr/bin/env bash

# yq
sudo apt install yq

# rockcraft
sudo snap install rockcraft --channel latest/edge --classic

# lxd
sudo snap install lxd
lxd --version
lxd init --auto

# charmcraft
sudo snap install charmcraft --channel latest/edge --classic

# microk8s
sudo snap install microk8s --channel 1.31-strict/stable
sudo adduser $USER snap_microk8s

# problem with running newgrp in scripts
# https://unix.stackexchange.com/questions/18897/problem-while-running-newgrp-command-in-script

/usr/bin/newgrp snap_microk8s <<EONG

# addons
# Required for Juju to provide storage volumes
sudo microk8s enable hostpath-storage
# Required to host the OCI image of the application
sudo microk8s enable registry
# Required to expose the application
sudo microk8s enable ingress

sudo microk8s status --wait-ready

# juju
sudo snap install juju --channel 3.6/stable
mkdir -p ~/.local/share
juju bootstrap microk8s dev

EONG