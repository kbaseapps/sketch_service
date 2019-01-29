import json
import tempfile
import os
import shutil
import flask
import traceback
from uuid import uuid4

from .exceptions import InvalidRequestParams
from .utils.autodownload import autodownload
from .utils.caching import upload_to_cache, get_cache_id, download_cache_string
from .utils.generate_sketch import generate_sketch
from .utils.perform_search import perform_search
from .config import load_config

app = flask.Flask(__name__)
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', True)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', str(uuid4()))

# AssemblyHomology database/namespace name to use
_db_name = os.environ.get('HOMOLOGY_NAMESPACE', 'NCBI_Refseq')


@app.route('/', methods=['POST', 'GET'])
def root():
    """
    JSON RPC v1.1 method call.
    Reference: https://jsonrpc.org/historical/json-rpc-1-1-wd.html
    We ignore the "method" parameter here as this service has only one function.
    """
    try:
        json_data = json.loads(flask.request.get_data())
    except Exception:
        raise InvalidRequestParams('Pass in a JSON body with RPC parameters.')
    auth_token = flask.request.headers.get('Authorization')
    method = json_data.get('method')
    if method == 'show_config':
        return show_config(json_data)
    elif method == 'get_homologs':
        return get_homologs(json_data, auth_token)
    else:
        resp = {
            'error': 'Invalid method. Valid methods are "get_homologs" or "show_config"',
            'version': '1.1'
        }
        return (flask.jsonify(resp), 400)


def get_homologs(json_data, auth_token):
    params = json_data.get('params')
    assert params and params.get('ws_ref'), "params must contain a 'ws_ref'"
    n_max_results = params.get('n_max_results', 10)
    # n_max_results argument must be an integer
    assert isinstance(n_max_results, int), "n_max_results must be an integer"
    if n_max_results < 1 or n_max_results > 100:
        print("n_max_results out of bounds (1< x < 100), resetting to 10")
        n_max_results = 10
    search_db = params.get('search_db', _db_name)

    ws_ref = params['ws_ref']
    tmp_dir = tempfile.mkdtemp()
    # Create unique identifying data for the cache
    cache_data = {'ws_ref': ws_ref, 'db_name': search_db, 'fn': 'get_homologs', 'n_max_results': n_max_results}
    cache_id = get_cache_id(cache_data)
    search_result_json = download_cache_string(cache_id)
    if not search_result_json or not search_result_json.strip():
        # If it is not cached, then we generate the sketch, perform the search, and cache it
        (data_path, paired_end) = autodownload(ws_ref, tmp_dir, auth_token)
        sketch_path = generate_sketch(data_path, search_db, paired_end)
        search_result = perform_search(sketch_path, search_db, n_max_results)
        search_result_json = json.dumps(search_result)
        if search_result_json:
            upload_to_cache(cache_id, search_result_json)
    shutil.rmtree(tmp_dir)  # Clean up all temp files
    return '{"version": "1.1", "result": ' + search_result_json + '}'


def show_config(json_data):
    config = load_config()
    config['service_token'] = bool(config['service_token'])
    return flask.jsonify({
        'result': config,
        'version': '1.1'
    })


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
def general_exception(err):
    trace = traceback.format_exc()
    resp = {
        'error': {
            'message': str(err),
            'trace': trace
        },
        'version': '1.1',
        'result': None
    }
    return (flask.jsonify(resp), 500)


@app.after_request
def after_request(resp):
    # Enable CORS
    resp.headers['Access-Control-Allow-Origin'] = '*'
    env_allowed_headers = os.environ.get('HTTP_ACCESS_CONTROL_REQUEST_HEADERS', 'Authorization, Content-Type')
    resp.headers['Access-Control-Allow-Headers'] = env_allowed_headers
    # Set JSON content type and response length
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Content-Length'] = resp.calculate_content_length()
    return resp
