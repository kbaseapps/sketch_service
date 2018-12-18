import json
import requests

from config import caching_service_url, service_token


def upload_to_cache(cache_id, string):
    """Save string content to a cache."""
    print('uploading string to cache', cache_id)
    print('string is', string)
    endpoint = caching_service_url + '/cache/' + cache_id
    bytestring = str.encode(string)
    resp = requests.post(
        endpoint,
        files={'file': ('data.txt', bytestring)},
        headers={'Authorization': service_token}
    )
    resp_json = resp.json()
    print('status is', resp_json['status'])
    if resp_json['status'] == 'error':
        raise Exception(resp_json['error'])


def get_cache_id(data):
    # Generate the cache_id
    print('generating a cache_id')
    headers = {'Content-Type': 'application/json', 'Authorization': service_token}
    endpoint = caching_service_url + '/cache_id'
    resp_json = requests.post(endpoint, data=json.dumps(data), headers=headers).json()
    if resp_json.get('error'):
        raise Exception(resp_json['error'])
    print('generated cache', resp_json)
    return resp_json['cache_id']


def download_cache_string(cache_id):
    """
    Fetch cached data as a string. Returns none if the cache does not exist.
    """
    endpoint = caching_service_url + '/cache/' + cache_id
    print('attempting to download cache', cache_id)
    resp = requests.get(endpoint, headers={'Authorization': service_token})
    if resp.status_code == 200:
        print('returning cached data')
        return resp.text
    else:
        print('cache does not exist')
