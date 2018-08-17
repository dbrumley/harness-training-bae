#!/bin/bash

set -eoux pipefail

minikube delete
sudo -E minikube start --vm-driver=none --cpus 4 --memory 8096
sudo chown -R $USER $HOME/.minikube
sudo chgrp -R $USER $HOME/.minikube
#kubectl create serviceaccount --namespace kube-system tiller
#kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
#kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'
echo core | sudo tee /proc/sys/kernel/core_pattern
cd /home/richard/training/mchart/
./scripts/dev/dev-install.sh
