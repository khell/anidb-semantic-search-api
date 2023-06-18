#!/bin/bash

## Only needed if you don't have a multiarch builder already
#docker buildx create --name multiarchbuilder --driver docker-container --bootstrap
#docker buildx use multiarchbuilder

docker buildx build --platform linux/amd64,linux/arm64 -t khell/anidb-semantic-search-api:latest --push .
