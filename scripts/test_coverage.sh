#!/bin/bash
source venv/bin/activate

python -m coverage run -m unittest discover tests
python -m coverage report
python -m coverage html

echo -e "\nHTML coverage report: $(pwd)/tmp/htmlcov/index.html"
