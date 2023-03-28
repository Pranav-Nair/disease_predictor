from flask import Flask
from flask_cors import CORS
from modelapi import mlcore
from webui import webapp
from resources import resource
app = Flask(__name__)
app.register_blueprint(mlcore)
app.register_blueprint(webapp)
app.register_blueprint(resource)
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)
