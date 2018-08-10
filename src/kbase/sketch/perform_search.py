import time
import os
import requests


def perform_search(sketch_path):
    """
    Make a request against the AssemblyHomologyService to do a search with a generated sketch file.
    """
    print('performing search..')
    start_time = time.time()
    homology_url = os.environ.get('KBASE_HOMOLOGY_URL', 'http://homology.kbase.us')
    namespace = 'NCBI_Refseq'
    path = '/namespace/' + namespace + '/search'
    with open(sketch_path, 'rb') as fd:
        response = requests.post(homology_url + path, data=fd)
    print('search done in', time.time() - start_time)
    return response.text
