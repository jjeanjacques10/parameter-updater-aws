#!/bin/bash

aws ssm put-parameter --name "/dev/onepiece-app/env" --value "PORT=8080;TIMEOUT_API_REQUEST=3000;TOGGLE_CARDS_OFFLINE=true" --type "String" --overwrite

echo "SSM parameters populated successfully."