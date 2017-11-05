#!/bin/bash
# Run local flask dev server

if [ ! -d venv ]; then
    echo 'script needs to be run from project base dir'
    exit
fi

source venv/bin/activate

export FLASK_CONFIG='config.DevConfig'
export FLASK_APP='app:app_from_envvar'
export FLASK_DEBUG=1

flask run
