import json
import requests
import os

_caching_server_url = os.environ.get('KBASE_CACHING_SERVER_URL', 'https://ci.kbase.us/services/cache/v1')
_service_token = os.environ['KB_SERVICE_TOKEN']
_headers = {'Content-Type': 'application/json', 'Authorization': _service_token}


def create_cache_sketch(cache_id, sketch_path):
    """Save a sketch file to a cache."""
    print('uploading a sketch file to a cache', cache_id)
    print('sketch path', sketch_path)
    endpoint = _caching_server_url + '/cache/' + cache_id
    print('sketch file size', os.path.getsize(sketch_path))
    with open(sketch_path, 'rb') as fd:
        resp = requests.post(
            endpoint,
            files={'file': fd},
            headers={'Authorization': _service_token}
        )
    resp_json = resp.json()
    print('status is', resp_json['status'])
    if resp_json['status'] == 'error':
        raise Exception(resp_json['error'])


def get_sketch_cache_id(ws_ref):
    # Generate the cache_id
    print('generating a cache_id for', ws_ref)
    cache_id_params = json.dumps({'function': 'generate_sketch', 'ws_ref': ws_ref})
    endpoint = _caching_server_url + '/cache_id'
    resp_json = requests.post(endpoint, data=cache_id_params, headers=_headers).json()
    if resp_json.get('error'):
        raise Exception(resp_json['error'])
    print('generated cache', resp_json)
    return resp_json['cache_id']


def download_cache_for_sketch(cache_id, save_dir):
    """
    Fetch a cached file, if it exists, given a workspace reference and a directory to save into.
    Returns the full path of the sketch file (the filename will be "sketch.msh")
    If the cache is missing, then None is returned.
    """
    endpoint = _caching_server_url + '/cache/' + cache_id
    print('attempting to download cache', cache_id)
    resp = requests.get(endpoint, headers={'Authorization': _service_token}, stream=True)
    size = 0
    if resp.status_code == 200:
        sketch_path = os.path.join(save_dir, 'sketch.msh')
        with open(sketch_path, 'wb') as fd:
            for chunk in resp.iter_content():
                size += len(chunk)
                fd.write(chunk)
        if size > 0:
            print('returning cached file')
            return sketch_path
        else:
            print('cache is empty')
