#!/bin/bash
# arg1 = config object to use (ex: "config.DevConfig")
# arg2 = action to perform (ex: migrate)
#
# example: ./scripts/migrate.sh config.DevConfig migrate

if [ $# -ne 2 ]; then
    echo "please provide config and action as args"
    exit
fi

source venv/bin/activate

export FLASK_CONFIG=$1
export FLASK_APP="app:app_from_envvar"
export FLASK_DEBUG=$(python -c "import config; print(1 if $FLASK_CONFIG.DEBUG else 0);")

flask db $2
