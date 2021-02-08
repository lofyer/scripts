#!/bin/bash
PLUGIN_LIST=$(grafana-cli plugins list-remote|grep "id:" | awk '{print $2}')
for i in $PLUGIN_LIST
do
    grafana-cli plugins install $i
done
