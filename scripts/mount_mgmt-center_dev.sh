#!/bin/bash

sudo mount -t cifs -o username=$2,password=$3 //$1/mgmt-center ~/mgmt-center_dev
