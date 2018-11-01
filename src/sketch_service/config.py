import urllib.parse
import os

kbase_endpoint = os.environ.get('KBASE_ENDPOINT', 'https://ci.kbase.us/services/')

service_token = os.environ['KBASE_SECURE_CONFIG_PARAM_service_token']

caching_service_url = os.environ.get(
    'KBASE_SECURE_CONFIG_PARAM_CACHING_SERVICE_URL',
    urllib.parse.urljoin(kbase_endpoint + '/', 'cache/v1')
)

id_mapper_url = os.environ.get(
    'KBASE_SECURE_CONFIG_PARAM_ID_MAPPER_URL',
    urllib.parse.urljoin(kbase_endpoint + '/', 'idmapper/api/v1')
)


print('Config data:')
print('-' * 80)
print('kbase_endpoint', kbase_endpoint)
print('len(service_token)', len(service_token))
print('caching_service_url', caching_service_url)
print('id_mapper_url', id_mapper_url)
print('-' * 80)
