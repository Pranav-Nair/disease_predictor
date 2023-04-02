from flask import Blueprint , send_from_directory
import os
resource = Blueprint("resource",__name__,url_prefix="/resource")

@resource.get("/img/<string:file>")
def send_img(file):
    if os.path.isfile("templates/website/img/"+file):
        return send_from_directory("templates/website/img", file)
    return 404
