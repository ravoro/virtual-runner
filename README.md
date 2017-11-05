# VirtualRunner

[![Build Status](https://travis-ci.org/ravoro/virtual-runner.svg?branch=master)](https://travis-ci.org/ravoro/virtual-runner)
[![Coverage Status](https://coveralls.io/repos/github/ravoro/virtual-runner/badge.svg?branch=master)](https://coveralls.io/github/ravoro/virtual-runner?branch=master)
[![BCH compliance](https://bettercodehub.com/edge/badge/ravoro/virtual-runner?branch=master)](https://bettercodehub.com/)

_You can now run **anywhere!**_

**VirtualRunner** is a website for keeping track of your run progress over a virtual map.

Utilizing the power of [Google Maps](https://developers.google.com/maps),
**VirtualRunner** brings you an **enhanced running experience**
by letting you plot out and follow your progress on virtual maps **anywhere in the world!**

## About
The website uses `Flask` backend with `SQLAlchemy` for dealing with the database.
The frontend is minimal and only uses JavaScript for dealing with Google Maps. 

## Usage
- Install project requirements - `pip install -r requirements.txt`
    - _You should install inside a [virtual environment](https://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs)_
- Copy the default configuration file `config.example.py` into `config.py` and set any customizations
- Set up the database schema - `./scripts/migrate.sh wsgi.py migrate`
- Start a dev server by running the standard `flask run` or custom `./scripts/run_dev.sh`
- To run on a production WSGI server, use the `wsgi.py` file

## Deployment
- `./scripts/deploy_latest.sh`

## Tests
- Run tests - `./scripts/test.sh`
- Run coverage - `./scripts/test_coverage.sh`
