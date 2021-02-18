import time
import os
import sys
import requests

from .map_refseq_ids import map_refseq_ids_to_kbase
from .map_strains import map_strains


def perform_search(sketch_path, db_name, max_results=10):
    """
    Make a request against the AssemblyHomologyService to do a search with a generated sketch file.
    """
    print('starting search request...')
    start_time = time.time()
    homology_url = os.environ.get('KBASE_HOMOLOGY_URL', 'https://homology.kbase.us')
    path = '/namespace/' + db_name + '/search'
    with open(sketch_path, 'rb') as fd:
        response = _retry_request(homology_url + path, fd, {'max': max_results})
    print('search done in', time.time() - start_time)
    resp_json = response.json()
    # Convert Refseq IDs into KBase IDs (only does these if we are in the refseq namespace)
    if db_name == "NCBI_Refseq":
        resp_json['distances'] = map_refseq_ids_to_kbase(resp_json['distances'])
        resp_json['distances'] = map_strains(resp_json['distances'])
    return resp_json


def _retry_request(url, data, params, max_retries=7):
    """
    Make a post request, retrying failures
    """
    tries = 0
    start = time.time()
    elapsed = 0
    while True:
        try:
            resp = requests.post(url, data=data, params=params, timeout=999)
            if resp.ok:
                return resp
        except Exception as err:
            sys.stderr.write(f"Error requesting AssemblyHomologyService: {err}\n")
            elapsed = time.time() - start
        tries += 1
        sys.stderr.write(f"Request to AssemblyHomologyService failed after {elapsed}s. Retrying..\n")
        if resp:
            sys.stderr.write(resp.text + '\n')
        if tries > max_retries:
            elapsed = time.time() - start
            raise RuntimeError(f"Failed requesting AssemblyHomologyService in {elapsed}s")
