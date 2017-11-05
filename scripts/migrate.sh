#!/bin/bash
# arg1 = flask app to use (ex: "wsgi.py")
# arg2 = action to perform (ex: migrate)
#
# example: ./scripts/migrate.sh wsgi.py migrate

if [ $# -ne 2 ]; then
    echo "please provide flask app and action as args"
    exit
fi

source venv/bin/activate
export FLASK_APP=$1
flask db $2
