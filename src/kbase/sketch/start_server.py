"""The main entrypoint for running the Flask server."""
import os
import flask
import subprocess
from dotenv import load_dotenv

load_dotenv('.env')

app = flask.Flask(__name__)
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', True)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


@app.before_request
def log_request():
    """Simple log of each request's response."""
    print(' '.join([flask.request.method, flask.request.path]))


@app.route('/', methods=['GET'])
def root():
    """Root path for the entire service"""
    out_str = subprocess.check_output(['mash'])
    return flask.jsonify({'hello': out_str})
