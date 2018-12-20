import json
import tempfile
import os
import shutil

from utils.autodownload import autodownload
from utils.caching import upload_to_cache, get_cache_id, download_cache_string
from utils.generate_sketch import generate_sketch
from utils.perform_search import perform_search

# AssemblyHomology database/namespace name to use
_db_name = os.environ.get('HOMOLOGY_NAMESPACE', 'NCBI_Refseq')


def get_homologs(params):
    """See 'get_homologs' inside kbase_methods.yaml."""
    auth_token = os.environ.get('KB_AUTH_TOKEN')
    ws_ref = params['upas'][0]
    tmp_dir = tempfile.mkdtemp()
    # Create unique identifying data for the cache
    cache_data = {'ws_ref': ws_ref, 'db_name': _db_name, 'fn': 'get_homologs'}
    cache_id = get_cache_id(cache_data)
    search_result_json = download_cache_string(cache_id)
    if search_result_json and search_result_json.strip():
        results = json.loads(search_result_json)
    else:
        # If it is not cached, then we generate the sketch, perform the search, and cache it
        (data_path, paired_end) = autodownload(ws_ref, tmp_dir, auth_token)
        sketch_path = generate_sketch(data_path, paired_end)
        results = perform_search(sketch_path, _db_name)
        if results:
            upload_to_cache(cache_id, json.dumps(results))
    shutil.rmtree(tmp_dir)  # Clean up all temp files
    return results
