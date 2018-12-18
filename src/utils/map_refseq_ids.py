import json
import requests

from config import id_mapper_url


def map_refseq_ids_to_kbase(distances):
    """
    Given the results from a request to the AssemblyHomologyService, iterate over every Refseq ID
    in the results and fetch the corresponding KBase ID using the ID Mapping service.
    Args:
      distances - an array of search result objects from the AssemblyHomologyService
    AssemblyHomology API: https://github.com/jgi-kbase/AssemblyHomologyService#api
    """
    # Create a list of Refseq IDs
    refseq_ids = [d['sourceid'] for d in distances]
    req_data = {"ids": refseq_ids}
    req_json = json.dumps(req_data)
    endpoint = id_mapper_url + '/mapping/RefSeq'
    print('Getting KBase IDs for', refseq_ids)
    print('  endpoint', endpoint)
    resp = requests.get(endpoint, data=req_json)
    # Handle any error case from the ID Mapper by exiting and logging everything
    if not resp.ok:
        print('=' * 80)
        print('ID Mapping error')
        print(resp.content)
        print(resp.status_code)
        print('=' * 80)
        raise Exception("Error from the ID Mapping service: " + resp.text)
    resp_json = resp.json()
    print('  response', resp.text)
    # Create a dict of indexes where each key is the refseq ID so we can refer to it below
    indexes = {}
    for (idx, dist) in enumerate(distances):
        indexes[dist['sourceid']] = idx
    # Find all KBase ids in the given mappings
    for (refseq_id, result) in resp_json.items():
        distance_idx = indexes[refseq_id]
        mappings = result['mappings']
        for mapping in mappings:
            if 'KBase' == mapping['ns']:
                kbase_id = mapping['id']
                distances[distance_idx]['kbase_id'] = kbase_id
    return distances
