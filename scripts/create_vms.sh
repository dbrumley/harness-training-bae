#!/bin/bash
set -euxo pipefail

NUM_USERS=16
ZONE=us-west1-a
gcloud config set project mayhem-training
for i in {1..16}
do
    #create disk from snapshot
    gcloud compute disks create user-$i-disk --source-snapshot snapshot-6 --zone $ZONE
    #create instance from disk
    gcloud compute instances create user-$i --disk name=user-$i-disk,boot=yes --machine-type n1-standard-8 --zone $ZONE
    #run reset script to reset minikube
    gcloud compute ssh --zone $ZONE user@user-$i --command="sudo -H -u user bash -c \"/home/user/mayhem-training/scripts/reset.sh\"" &
    #change mayhem-client.cfg
    #gcloud compute ssh --zone $ZONE user@user-$i --command="echo -e \"[mayhemdb]\nurl=\`minikube service \$(kubectl get services -l tier=frontend -o name | cut -d/ -f2) --url\`\" > ~/.mayhem-client.cfg" 
done
 
