from flask import Flask
from modelapi import mlcore
app = Flask(__name__)
app.register_blueprint(mlcore)

if __name__ == "__main__":
    app.run(debug=True)
