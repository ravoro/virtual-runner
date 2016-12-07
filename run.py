from app import app

app.config.from_object("config.DevConfig")
app.run()
