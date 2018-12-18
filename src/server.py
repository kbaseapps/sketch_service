import json
import time
import tempfile
import os
import shutil
import flask
import traceback
from uuid import uuid4

from kbase_workspace_utils.exceptions import InvalidUser, InaccessibleWSObject, InvalidGenome
from .autodownload import autodownload
from .caching import upload_to_cache, get_cache_id, download_cache_string
from .exceptions import InvalidRequestParams, UnrecognizedWSType
from .generate_sketch import generate_sketch
from .perform_search import perform_search

os.environ['KBASE_ENV'] = os.environ.get('KBASE_ENV', 'appdev')
app = flask.Flask(__name__)
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', True)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', str(uuid4()))

# AssemblyHomology database/namespace name to use
db_name = os.environ.get('HOMOLOGY_NAMESPACE', 'NCBI_Refseq')


@app.route('/', methods=['POST', 'GET'])
def root():
    """
    JSON RPC v1.1 method call.
    Reference: https://jsonrpc.org/historical/json-rpc-1-1-wd.html
    We ignore the "method" parameter here as this service has only one function.
    """
    start_time = time.time()
    json_data = flask.request.get_json()
    print('performing search..')
    if not json_data:
        raise InvalidRequestParams('Pass in a JSON body with RPC parameters.')
    # if not flask.request.headers.get('Authorization'):
        # raise InvalidRequestParams('The Authorization header must contain a KBase auth token.')
    auth_token = flask.request.headers.get('Authorization')
    if not json_data.get('params'):
        raise InvalidRequestParams('.params must be a list of one workspace reference.')
    ws_ref = json_data['params'][0]
    tmp_dir = tempfile.mkdtemp()
    # Create unique identifying data for the cache
    cache_data = {'ws_ref': ws_ref, 'db_name': db_name, 'fn': 'get_homologs'}
    cache_id = get_cache_id(cache_data)
    search_result_json = download_cache_string(cache_id)
    if not search_result_json:
        # If it is not cached, then we generate the sketch, perform the search, and cache it
        (data_path, paired_end) = autodownload(ws_ref, tmp_dir, auth_token)
        sketch_path = generate_sketch(data_path, paired_end)
        search_result = perform_search(sketch_path, db_name)
        search_result_json = json.dumps(search_result)
        if search_result_json:
            upload_to_cache(cache_id, search_result_json)
    shutil.rmtree(tmp_dir)  # Clean up all temp files
    print('total request time:', time.time() - start_time)
    return '{"version": "1.1", "result": ' + search_result_json + '}'


@app.errorhandler(InvalidUser)
@app.errorhandler(UnrecognizedWSType)
@app.errorhandler(InvalidGenome)
@app.errorhandler(InaccessibleWSObject)
@app.errorhandler(InvalidRequestParams)
def invalid_user(err):
    """Generic exception catcher, returning 400."""
    resp = {
        'version': '1.1',
        'error': str(err),
        'result': None
    }
    return (flask.jsonify(resp), 400)


@app.errorhandler(404)
def page_not_found(err):
    """Return a JSON data for 404."""
    resp_data = {
        'version': '1.1',
        'error': 'Endpoint does not exist. Make a JSON RPC call to the root path.',
        'result': None
    }
    return (flask.jsonify(resp_data), 404)


@app.errorhandler(Exception)
def any_exception(err):
    """A catch-all for any exceptions we didn't explicitly handle above."""
    traceback.print_exc()
    resp = {
        'version': '1.1',
        'error': str(err),
        'result': None
    }
    return (flask.jsonify(resp), 500)


@app.after_request
def after_request(resp):
    # Enable CORS
    resp.headers['Access-Control-Allow-Origin'] = '*'
    env_allowed_headers = os.environ.get('HTTP_ACCESS_CONTROL_REQUEST_HEADERS', 'authorization')
    resp.headers['Access-Control-Allow-Headers'] = env_allowed_headers
    # Set JSON content type and response length
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Content-Length'] = resp.calculate_content_length()
    return resp
