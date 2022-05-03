#!/bin/bash

projectName="agent"
namespace="chp"

export $(egrep -v '^#' .env)

sed -i.bak \
    -e "s/DOCKER_VERSION_VALUE/${BUILD_VERSION}/g" \
    values.yaml
rm values.yaml.bak

helm -n ${namespace} upgrade --install ${projectName} -f values.yaml -f values-ci.yaml ./
