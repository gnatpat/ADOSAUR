#!/bin/bash

mkdir tmp

# Install dependencies for Backend
echo "Installing Backend dependencies"
cd app/backend
npm i
npm i grunt-cli

echo "Installing Frontend dependencies"
# Install dependencies for Frontend
cd ../frontend/
npm i

echo "Installing Python dependencies"
# Install python packages
pip install --user liac-arff
pip install --user numpy
pip install --user matplotlib
pip install --user --upgrade https://github.com/Theano/Theano/archive/master.zip
pip install --user --upgrade https://github.com/Lasagne/Lasagne/archive/master.zip
pip install --user git+https://github.com/dnouri/nolearn.git@master#egg=nolearn==0.7.git
