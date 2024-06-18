#!/bin/bash

#Find root directory of the project
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

#Deactivate virtual environment if exists
if [ -d "$ROOT_DIR/venv" ]; then
    source deactivate
    rm -rf $ROOT_DIR/venv
    echo "Deactivated existing virtual environment"
fi

#Create a python virtual environment
python3 -m venv $ROOT_DIR/venv
echo "Virtual environment created"

#Activate the virtual environment
source $ROOT_DIR/venv/bin/activate

#Install the required packages
pip install -r $ROOT_DIR/requirements.txt

#Set the environment variables from .env file
set -a
source $ROOT_DIR/.env
set +a
