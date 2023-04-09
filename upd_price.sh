#!/bin/bash

home_dir=$pwd
sleep 2
# update the file
curl -i -X PUT -H 'Authorization: token '$1 -d "{\"path\": \"lowest.txt\", \
\"message\": \"update\", \"content\": \"$(openssl base64 -A -in ./lowest.txt)\", \"branch\": \"feature/updated_prices\",\
\"sha\": $(curl -X GET https://api.github.com/repos/anoop-kmr/ltdinia/contents/lowest.txt?ref=feature/updated_prices | jq .sha)}" \
https://api.github.com/repos/anoop-kmr/ltdinia/contents/lowest.txt?ref=feature/updated_prices
