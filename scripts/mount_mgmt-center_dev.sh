#!/bin/bash

sudo mount -t cifs -o username=$2,password=$3 //$1/mgmt-project ~/mgmt-center_dev
