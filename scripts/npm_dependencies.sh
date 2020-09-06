#!/bin/bash
cd ..
cd cloned_git
npm install -s
npm list --depth 0 -s > npm_dependencies.txt
cd ..
cd src