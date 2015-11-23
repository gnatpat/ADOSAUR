#!/bin/bash

# Install dependencies for Backend
echo "Installing Backend dependencies"
cd app/Backend
npm i
npm i grunt-cli

echo "Installing Frontend dependencies"
# Install dependencies for Frontend
cd ../Frontend/
npm i

echo "Installing Python dependencies"
# Install python packages
pip install --user liac-arff
pip install --user numpy
pip install --user matplotlib
