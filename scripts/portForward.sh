#!/usr/bin/env bash

function usage {
  echo "USAGE: portForward.sh <instance-name> <ip-address> <port-number>"
}

function enable_ip_forward {
  forward_status=$(multipass exec $1 -- sysctl net.ipv4.ip_forward | sed -n 's/.*=\s\?\([0-1]\)/\1/p')
  if [ "$forward_status" -eq "0" ]; then
    multipass exec $1 -- sudo sysctl -w net.ipv4.ip_forward=1
  fi
}

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    usage
    exit 1
fi

# Enable ip forwarding in the VM
enable_ip_forward $1

# Dynamic NAT: redirect incoming packets to the internal IP
multipass exec $1 -- sudo iptables -t nat -A PREROUTING -p tcp --dport $3 -j DNAT --to-destination $2:$3
# Allow forwarding from host side to the Kubernetes interface (e.g., cni0)
multipass exec $1 -- sudo iptables -A FORWARD -p tcp -d $2 --dport $3 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
# Return traffic handling
multipass exec $1 -- sudo iptables -A FORWARD -p tcp -s $2 --sport $3 -m state --state ESTABLISHED,RELATED -j ACCEPT

# Save changes to make them permanent
multipass exec $1 -- sudo iptables-save
