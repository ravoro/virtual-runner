import os
import sys

BASE_DIR = os.path.dirname(__file__)

# enable venv
activate_this = os.path.join(BASE_DIR, 'venv', 'bin', 'activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# add application location to system path
sys.path.insert(0, BASE_DIR)
from app import create_app

# create application
application = create_app("config.ProdConfig")
