import tempfile
import os
import shutil
import flask
from uuid import uuid4

from utils.caching import upload_to_cache, get_cache_id, download_cache_string
from utils.autodownload import autodownload
from utils.generate_sketch import generate_sketch
from utils.perform_search import perform_search

os.environ['KBASE_ENV'] = os.environ.get('KBASE_ENV', 'appdev')
app = flask.Flask(__name__)
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', True)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', str(uuid4()))

# AssemblyHomology database/namespace name to use
_db_name = os.environ.get('HOMOLOGY_NAMESPACE', 'NCBI_Refseq')


def sketch_and_search(params):
    """
    Create and cache a mash sketch for a reads, assembly, or genome and search
    it against a database of other sketches.

    Params is an array of workspace object addresses (1/2/3).
    """
    results = {}
    auth_token = os.environ.get('KB_AUTH_TOKEN')
    for upa in params['upas']:
        tmp_dir = tempfile.mkdtemp()
        cache_data = {'obj': upa, 'db_name': _db_name, 'fn': 'sketch_and_search'}
        cache_id = get_cache_id(cache_data)
        search_result_json = download_cache_string(cache_id)
        if not search_result_json:
            # If it is not cached, then we generate the sketch, perform the search, and cache it
            (data_path, paired_end) = autodownload(upa, tmp_dir, auth_token)
            sketch_path = generate_sketch(data_path, paired_end)
            search_result_json = perform_search(sketch_path, _db_name)
            if search_result_json:
                upload_to_cache(cache_id, search_result_json)
        shutil.rmtree(tmp_dir)
        results[upa] = search_result_json
    return results
