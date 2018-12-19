import os
from urllib.parse import urljoin

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
