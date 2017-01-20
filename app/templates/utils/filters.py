from app import app


@app.template_filter()
def asset_release_version(url):
    version = app.config['RELEASE_VERSION']
    if version:
        url = "{}?v={}".format(url, version)
    return url
