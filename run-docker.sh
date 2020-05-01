#!/bin/bash
docker run -d \
  --name datadrop \
  -v /mnt/datadrop-static:/static \
  -v /mnt/datadrop-data:/data \
  -v /mnt/datadrop-uploads:/uploads \
  -v `pwd`/settings-prod.py:/code/datadrop/settings-prod.py \
  --publish 127.0.0.1:8000:8000 \
  datadrop:latest

