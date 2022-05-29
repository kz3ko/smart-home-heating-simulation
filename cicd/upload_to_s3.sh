#! /bin/bash

cd ..
zip -r app.zip app

aws s3 cp app.zip s3://smart-home-simulation-bucket-eu-west-1/app.zip
aws s3 cp infrastructure/setup_script.sh s3://smart-home-simulation-bucket-eu-west-1/setup_script.sh
