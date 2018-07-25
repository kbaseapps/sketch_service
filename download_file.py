"""
Download a file from Shock ID (KBase uses a file server called "shock", which has object IDs for
its files).
"""
import os
import tempfile
import requests


def download_file(shock_id, auth_token):
    # Make a request to the workspace (?) to get the file and put it in /tmp
    shock_url = os.environ['KBASE_SHOCK_URL']
    node_url = shock_url + '/node/' + shock_id + '?download_raw'
    headers = {'Authorization': 'OAuth ' + auth_token}
    response = requests.get(
        node_url,
        headers=headers,
        allow_redirects=True,
        stream=True
    )
    with tempfile.NamedTemporaryFile() as tmp_file:
        tmp_file.write('stuff')
        for chunk in response.iter_content(1024):
            if not chunk:
                break
            tmp_file.write(chunk)
    return tmp_file.name

