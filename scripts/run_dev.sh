#!/bin/bash
# Run local flask dev server

if [ ! -d venv ]; then
    echo 'script needs to be run from project base dir'
    exit
fi

source venv/bin/activate

export FLASK_APP='wsgi_dev.py'
export FLASK_DEBUG=1

flask run
