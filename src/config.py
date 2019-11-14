import os
from urllib.parse import urljoin

from kbase_cache_client import KBaseCacheClient


def load_config():
    kbase_endpoint = os.environ.get('KBASE_ENDPOINT', 'https://ci.kbase.us/services')
    service_token = os.environ['KBASE_SECURE_CONFIG_PARAM_service_token']
    caching_service_url = os.environ.get(
        'KBASE_SECURE_CONFIG_PARAM_CACHING_SERVICE_URL',
        urljoin(kbase_endpoint + '/', 'cache/v1')
    )
    id_mapper_url = os.environ.get(
        'KBASE_SECURE_CONFIG_PARAM_ID_MAPPER_URL',
        urljoin(kbase_endpoint + '/', 'idmapper/api/v1')
    )
    workspace_url = kbase_endpoint + '/ws'
    homology_url = os.environ.get('KBASE_HOMOLOGY_URL', 'https://homology.kbase.us')
    client = KBaseCacheClient(kbase_endpoint, token=service_token)
    return {
        'homology_url': homology_url,
        'id_mapper_url': id_mapper_url,
        'caching_service_url': caching_service_url,
        'workspace_url': workspace_url,
        'service_token': service_token,
        'kbase_endpoint': kbase_endpoint,
        'cache_client': client
    }
