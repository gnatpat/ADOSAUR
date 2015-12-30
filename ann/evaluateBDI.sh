#!/bin/sh

touch tmp/trash

INPUT=$1
cd openSMILE
./extract.sh ../$INPUT > ../tmp/trash 2>&1
cd ..
python evaluateArff.py
rm -f openSMILE/output.arff tmp/trash
