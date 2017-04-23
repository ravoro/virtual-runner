#!/bin/bash
# Run `mymy` for optional type checking

if [ ! -d venv ]; then
    echo 'script needs to be run from project base dir.'
    echo 'also, ensure that you have a "venv" directory with python3 installed'
    exit
fi

source venv/bin/activate
mypy --strict-optional --ignore-missing-imports app
