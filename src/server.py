import json
import tempfile
import os
import shutil
import flask
import traceback
from uuid import uuid4

from src.exceptions import InvalidJSON, InvalidParams, UnknownMethod
from src.utils.autodownload import autodownload
from src.utils.caching import upload_to_cache, get_cache_id, download_cache_string
from src.utils.generate_sketch import generate_sketch
from src.utils.perform_search import perform_search
from src.config import load_config

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
    """
    try:
        json_data = json.loads(flask.request.get_data())
    except Exception:
        raise InvalidJSON('Unable to parse JSON request body.')
    auth_token = flask.request.headers.get('Authorization')
    # Return the method name without any module name
    method = json_data.get('method').split('.')[-1]
    print(f'{flask.request.method} {flask.request.path} -> {method}')
    handler = _METHODS.get(method)
    if not handler:
        raise UnknownMethod(json_data.get('id'), f'Unknown method "{method}"')
    return handler(json_data, auth_token)  # type: ignore


def get_homologs(json_data, auth_token):
    params = json_data.get('params')
    if not params.get('ws_ref'):
        raise InvalidParams(json_data.get('id'), f"Params must contain `ws_ref` (workspace object reference)")
    n_max_results = params.get('n_max_results', 10)
    bypass_caching = params.get('bypass_caching', False)
    # n_max_results argument must be an integer
    if not isinstance(n_max_results, int):
        raise InvalidParams(json_data.get('id'), f"`n_max_results` must be an integer")
    search_db = params.get('search_db', _db_name)
    ws_ref = params['ws_ref']
    print(f"Fetching homologs for object {ws_ref}")
    tmp_dir = tempfile.mkdtemp()
    # Create unique identifying data for the cache
    cache_data = {
        'ws_ref': ws_ref,
        'db_name': search_db,
        'fn': 'get_homologs',
        'n_max_results': n_max_results
    }
    cache_id = get_cache_id(cache_data)

    def sketch_search_cache(cache_):
        # If it is not cached, then we generate the sketch, perform the search, and cache it
        (data_path, paired_end) = autodownload(ws_ref, tmp_dir, auth_token)
        sketch_path = generate_sketch(data_path, search_db, paired_end)
        search_result = perform_search(sketch_path, search_db, n_max_results)
        if search_result and cache_:
            upload_to_cache(cache_id, json.dumps(search_result))
        return search_result

    if bypass_caching:
        print('Bypassing the cache and performing the search')
        search_result = sketch_search_cache(False)
    else:
        try:
            cached = download_cache_string(cache_id)
            search_result = json.loads(cached)
            print("Fetched search results from the cache")
        except Exception:
            print("Cannot load results from the cache; performing new search")
            search_result = sketch_search_cache(True)
    shutil.rmtree(tmp_dir)  # Clean up all temp files
    return flask.jsonify({
        'version': '1.1',
        'id': json_data.get('id'),
        'result': search_result
    })


def show_config(json_data, auth_token=None):
    config = load_config()
    # Explicitly write in config entries we want to return. Do not show anything private.
    result = {
        'homology_url': config['homology_url'],
        'id_mapper_url': config['id_mapper_url'],
        'caching_service_url': config['caching_service_url'],
        'kbase_endpoint': config['kbase_endpoint'],
        'cache_client': config['client']
    }
    return flask.jsonify({
        'version': '1.1',
        'id': json_data.get('id'),
        'result': result
    })


@app.errorhandler(InvalidParams)
@app.errorhandler(UnknownMethod)
def invalid_request(err):
    error = {
        'name': getattr(err, 'name') or 'InvalidRequest',
        'message': getattr(err, 'message')
    }
    resp = {
        'version': '1.1',
        'id': getattr(err, 'req_id'),
        'error': error
    }
    return (flask.jsonify(resp), 400)


@app.errorhandler(404)
def page_not_found(err):
    """Return a JSON data for 404."""
    resp_data = {
        'version': '1.1',
        'error': {
            'name': 'NotFound',
            'message': 'Endpoint does not exist. Make a JSON RPC call to the root path.',
        }
    }
    return (flask.jsonify(resp_data), 404)


# RPC method names (without any module name) mapped to function handlers
_METHODS = {
    'get_homologs': get_homologs,
    'show_config': show_config
}


@app.errorhandler(Exception)
def general_exception(err):
    traceback.print_exc()
    resp = {
        'error': {
            'message': str(err),
            'name': err.__class__.__name__
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


def _unknown_method_resp(method, json_data):
    resp = {
        'error': {
            'name': 'UnknownMethod',
            'message': 'Unknown method "{method}"'
        },
        'id': json_data.get('id'),
        'version': '1.1'
    }
    return (flask.jsonify(resp), 400)
