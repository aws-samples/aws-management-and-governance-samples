#!/bin/bash

rm -rf ./lambda_sources/function/lib
pip3 install -r ./lambda_sources/function/lambda_requirements.txt -t ./lambda_sources/function/lib/
cp ./lambda_sources/function/*.py ./lambda_sources/function/lambda_requirements.txt ./lambda_sources/function/lib/ &&
cd ./lambda_sources/function/lib && zip -r  ../../packaged_lambda_assets/sources.zip .
cd ../../layers && zip -r ../packaged_lambda_assets/opa.zip .
