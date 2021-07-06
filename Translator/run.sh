#!/bin/bash

echo "working dir:- $(pwd)"
cd $(pwd)
echo "---------------Installing requirements-------------"
git pull origin main
echo "---------------Installing requirements-------------"
echo "---------------Installing easynmt------------------"
pip install easynmt
echo "---------------Installing flask-ngrok------------------"
pip install flask-ngrok
echo "---------------RUN main.py------------------"
#python main.py
echo "---------------RUN app.py------------------"
python $(pwd)/app.py 

