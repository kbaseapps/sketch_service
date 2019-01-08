import time
import os
import requests

from .map_refseq_ids import map_refseq_ids_to_kbase


def perform_search(sketch_path, db_name, n_max_results):
    """
    Make a request against the AssemblyHomologyService to do a search with a generated sketch file.
    """
    print('starting search request...')
    start_time = time.time()
    homology_url = os.environ.get('KBASE_HOMOLOGY_URL', 'https://homology.kbase.us')
    path = '/namespace/' + db_name + '/search' + '?max=' + str(n_max_results) 
    with open(sketch_path, 'rb') as fd:
        response = requests.post(homology_url + path, data=fd)
    print('search done in', time.time() - start_time)
    if response.status_code == 200:
        resp_json = response.json()
        # Convert Refseq IDs into KBase IDs
        resp_json['distances'] = map_refseq_ids_to_kbase(resp_json['distances'])
        return resp_json
    else:
        raise Exception('Error performing search: ' + response.text)
