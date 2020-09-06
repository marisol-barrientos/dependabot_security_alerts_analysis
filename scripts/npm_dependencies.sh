#!/bin/bash
cd ..
cd output
npm install -s
npm list --depth 0 -s > npm_dependencies.txt
cd ..
cd src