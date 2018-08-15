#!/bin/bash
set -euxo pipefail

NUM_USERS=5
gcloud config set project mayhem-training
for i in `seq 1 $NUM_USERS`
do
    gcloud compute disks create user-$i-disk --source-snapshot training-base --zone us-west1-a
    gcloud compute instances create user-$i --disk name=user-$i-disk,boot=yes --machine-type n1-standard-8 --zone us-west1-a
done
 
