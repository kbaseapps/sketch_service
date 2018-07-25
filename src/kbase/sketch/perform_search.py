import os
import requests


def perform_search(sketch_result):
    """
    """
    homology_url = os.environ['KBASE_HOMOLOGY_URL']
    path = "/namespace/KBase_Refseq/search"
    with open(sketch_result.path, 'rb') as readf:
        response = requests.post(
            homology_url + path,
            data=readf
        )
    return response.text
