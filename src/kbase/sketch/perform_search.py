import os
import requests


def perform_search(sketch_result):
    """
    Make a request against the AssemblyHomologyService to do a search with a generated sketch file.
    """
    homology_url = os.environ['KBASE_HOMOLOGY_URL']
    namespace = 'NCBI_Refseq'
    path = '/namespace/' + namespace + '/search'
    with open(sketch_result.path, 'rb') as readf:
        response = requests.post(homology_url + path, data=readf)
    return response.text
