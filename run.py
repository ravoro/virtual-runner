from app import create_app
from flask_debugtoolbar import DebugToolbarExtension

app = create_app("config.DevConfig")

# initialize debugtoolbar
DebugToolbarExtension(app)

app.run()
