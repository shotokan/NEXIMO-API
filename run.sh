#!/usr/bin/env bash

set -e
pip install -r ./requirements.txt
python3 db_script.py
gunicorn -b 0.0.0.0:5000 main:app