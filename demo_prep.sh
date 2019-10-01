#!/bin/bash

rm -rf venv
virtualenv --python=$(which python3.7) venv
source venv/bin/activate

pip install --upgrade git+https://github.com/ansible/ansible
