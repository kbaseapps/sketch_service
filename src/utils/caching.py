import tempfile

from src.config import load_config


def upload_to_cache(cache_id, string):
    """Save string content to a cache."""
    config = load_config()
    print(f'Uploading contents to cache {cache_id[0:16]}..')
    config['cache_client'].upload_cache(cache_id, string=string)


def get_cache_id(data):
    # Generate the cache_id
    config = load_config()
    cache_id = config['cache_client'].generate_cacheid(data)
    print(f'Fetched cache ID {cache_id[0:16]}..')
    return cache_id


def download_cache_string(cache_id):
    """
    Fetch cached data as a string. Returns none if the cache does not exist.
    """
    config = load_config()
    with tempfile.NamedTemporaryFile() as fd:
        config['cache_client'].download_cache(cache_id, fd.name)
        contents = fd.read().decode()
        print(f'Downloaded contents from cache ID {cache_id[0:16]}..')
        return contents
