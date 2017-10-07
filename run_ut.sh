#!/bin/bash
set -e
if [ -z "$VIRTUAL_ENV" ]; then
    virtualenv .ut_venv
    source .ut_venv/bin/activate
fi

export PYTHONPATH="./proj1:./proj1/proj1:."

pip install -r requirements.txt

python ./proj1/manage.py test proj1/proj1/