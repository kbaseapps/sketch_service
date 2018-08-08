import tempfile
import os
import shutil
import flask
import traceback
from dotenv import load_dotenv

from kbase_workspace_utils.exceptions import InvalidUser, InaccessibleWSObject, InvalidGenome
from .autodownload import autodownload
from .exceptions import InvalidRequestParams, UnrecognizedWSType
from .generate_sketch import generate_sketch
from .perform_search import perform_search

load_dotenv()

print('=' * 100)
print('os.environ', os.environ)
print('=' * 100)
os.environ['KBASE_ENV'] = os.environ.get('KBASE_ENV', 'appdev')
app = flask.Flask(__name__)
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', True)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


@app.route('/', methods=['POST'])
def root():
    """
    JSON RPC v1.1 method call.
    Reference: https://jsonrpc.org/historical/json-rpc-1-1-wd.html
    We ignore the "method" parameter here as this service has only one function.
    """
    json_data = flask.request.get_json()
    if not flask.request.headers.get('Authorization'):
        raise InvalidRequestParams('The Authorization header must be a KBase auth token.')
    auth_token = flask.request.headers['Authorization']
    if not json_data.get('params'):
        raise InvalidRequestParams('.params must be a list of one workspace reference.')
    ws_ref = json_data['params'][0]
    # For each sketch, we make and remove a temporary directory
    tmp_dir = tempfile.mkdtemp()
    (path, paired_end) = autodownload(ws_ref, tmp_dir, auth_token)
    sketch_result = generate_sketch(path, paired_end)
    search_result = perform_search(sketch_result)
    shutil.rmtree(tmp_dir)  # Clean up temp files
    return '{"version": "1.1", "result": ' + search_result + '}'


@app.errorhandler(InvalidUser)
@app.errorhandler(UnrecognizedWSType)
@app.errorhandler(InvalidGenome)
@app.errorhandler(InaccessibleWSObject)
@app.errorhandler(InvalidRequestParams)
def invalid_user(err):
    """Generic exception catcher, returning 400."""
    return (flask.jsonify({'version': '1.1', 'error': str(err)}), 400)


@app.errorhandler(404)
def page_not_found(err):
    """Return a JSON data for 404."""
    resp_data = {
        'version': '1.1',
        'error': 'Endpoint does not exist. Make a JSON RPC call to the root path.'
    }
    return (flask.jsonify(resp_data), 404)


@app.errorhandler(Exception)
def any_exception(err):
    """A catch-all for any exceptions we didn't explicitly handle above."""
    traceback.print_exc()
    return (flask.jsonify({'version': '1.1', 'error': str(err)}), 500)
