#!/bin/bash

sudo mount -t cifs -o username=$1,password=$2 //192.168.178.21/mgmt-project ~/mgmt-center_dev
