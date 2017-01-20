#!/bin/bash

cd $sites/virtual-runner
source venv/bin/activate
del journeys.db
python -c "from app import db; db.create_all();"
#sqlite3 journeys.db < init.sql
