from flask import Blueprint , send_from_directory
import os
resource = Blueprint("resource",__name__,url_prefix="/resource")

@resource.get("/js/<string:file>")
def send_js(file):
    return send_from_directory("templates/website/js", file)


@resource.get("/lib")
def send_js_lib():
    return send_from_directory("templates/website/js/lib","jquery-3.6.4.min.js")


@resource.get("/img/<string:file>")
def send_img(file):
    if os.path.isfile("templates/website/img/"+file):
        return send_from_directory("templates/website/img", file)
    return 404
