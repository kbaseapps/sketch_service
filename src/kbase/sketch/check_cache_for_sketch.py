import os
import json
import requests

caching_server_url = "https://ci.kbase.us/cache/v1"


def check_cache_for_sketch(ws_ref, save_dir):
    auth_token = os.environ['KB_AUTH_TOKEN']
    # Generate the cache_id
    cache_params = {'function': 'generate_sketch', 'ws_ref': ws_ref}
    headers = {'Authorization': auth_token, 'Content-Type': 'application/json'}
    resp_json = requests.post(caching_server_url + '/cache_id', data=json.dumps(cache_params), headers=headers).json()
    cache_id = resp_json['cache_id']
    resp = requests.get(
        caching_server_url + '/cache/' + cache_id + '/info',
        headers=headers
    )
    if resp.status_code == 200:
        sketch_path = os.path.join(save_dir, 'sketch.msh')
        with open(sketch_path, 'wb') as fd:
            for chunk in resp.iter_content():
                fd.write(chunk)
        return sketch_path
