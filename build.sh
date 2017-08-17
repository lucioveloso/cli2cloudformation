#!/usr/bin/env bash

f=cli2cfnLambda
rm -rf $f
mkdir $f
pip install awscli -t $f
pip install requests -t $f
cp wrapper index.py $f
cd $f
zip -r ../$f.zip .
cd ..
rm -rf $f
