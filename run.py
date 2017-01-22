from app import app
from flask_debugtoolbar import DebugToolbarExtension

app.config.from_object("config.DevConfig")

toolbar = DebugToolbarExtension(app)

app.run()
