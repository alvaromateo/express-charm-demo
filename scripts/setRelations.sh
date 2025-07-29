juju status | grep -q "^${express_charm_name}\\s"
if [ $? -eq 0 ]; then
  echo "Application ${express_charm_name} exists. Running juju refresh..."
  juju refresh ${appname} --path ./charm/${charmname}_${archname}.charm --resource app-image=localhost:32000/${rockname}:${version}
else
  echo "Application '$appname' does not exist. Running juju deploy..."
  juju deploy ./charm/${charmname}_${archname}.charm ${appname} --resource app-image=localhost:32000/${rockname}:${version}
fi