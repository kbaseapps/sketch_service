import os
import tempfile
import requests
from collections import namedtuple


# A successfully downloaded file
DownloadedFile = namedtuple('DownloadedFile', ['dir_path', 'file_name', 'file_path'])

# The result, with possible error, of downloading a shock file
DownloadResult = namedtuple('DownloadResult', ['error', 'downloaded_file'])


def get_node_url(shock_id):
    """
    Get the url of a node on Shock. A node is a file object with an ID.
    The KBASE_SHOCK_URL env var must be set.
    """
    shock_url = os.environ['KBASE_SHOCK_URL']
    return shock_url + '/node/' + shock_id


def download_file_metadata(shock_id, auth_token):
    """
    Download the file metadata from shock:
    Args:
      shock_id is the unique ID of a shock object
      auth_token is TODO
    """
    node_url = get_node_url(shock_id)
    response = requests.get(node_url, allow_redirects=True)
    return response.json()


def download_file(shock_id, auth_token):
    """
    Download a file from shock.
    Args:
      shock_id is the unique ID of a shock object, pointing to a fasta/fastq file
      auth_token is TODO
    """
    # headers = {'Authorization': 'OAuth ' + auth_token}
    # First, we need to make a request to check for the existence of the file and get its name
    metadata = download_file_metadata(shock_id, auth_token)
    node_url = get_node_url(shock_id)
    if metadata['status'] == 404:
        return DownloadResult(error='File not found', downloaded_file=None)
    name = metadata['data']['file']['name']
    # Download the actual file
    response = requests.get(
        node_url + '?download_raw',
        # headers=headers,
        allow_redirects=True,
        stream=True
    )
    dir_path = tempfile.mkdtemp()
    file_path = os.path.join(dir_path, name)
    with open(file_path, 'wb') as fwrite:
        for block in response.iter_content(1024):
            fwrite.write(block)
    downloaded_file = DownloadedFile(dir_path=dir_path, file_name=name, file_path=file_path)
    return DownloadResult(downloaded_file=downloaded_file, error=None)
