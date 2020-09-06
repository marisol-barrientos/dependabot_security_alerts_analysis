#!/bin/bash
cd ..
cd output
yarn install -s
yarn list --depth 0 -s > yarn_dependencies.txt
cd ..
cd src