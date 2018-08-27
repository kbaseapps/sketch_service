"""
Simple integration tests on the API itself.

We make actual ajax requests to the running docker container.
"""
import os
import json
import unittest
import requests
from dotenv import load_dotenv

load_dotenv('.env')


# The URL of the running server from within the docker container
url = 'http://0.0.0.0:5000'
service_token = os.environ['KB_SERVICE_TOKEN']
os.environ['KB_SERVICE_TOKEN'] = ''


def make_request(ws_ref):
    """Helper to make a JSON RPC request with the given workspace ref."""
    post_data = {'params': [ws_ref], 'method': 'get_homologs', 'id': 0}
    headers = {'Content-Type': 'application/json', 'Authorization': service_token}
    resp = requests.post(url, data=json.dumps(post_data), headers=headers)
    return resp.json()


class TestApi(unittest.TestCase):

    def test_search_reads_paired(self):
        """Test a search on genome read data with paired-ends."""
        reads_ref = '15/45/1'
        json_resp = make_request(reads_ref)
        print('-' * 80)
        print(json_resp)
        print('-' * 80)
        result = json_resp['result']
        self.assertTrue(len(result['distances']))

    def test_search_reads_single(self):
        """Test a search on single-ended genome read data."""
        reads_ref = '15/43/1'
        json_resp = make_request(reads_ref)
        print('-' * 80)
        print(json_resp)
        print('-' * 80)
        result = json_resp['result']
        self.assertTrue(len(result['distances']))

    def test_search_genome(self):
        """Test a search on a Genome type."""
        genome_ref = '34819/14/1'
        json_resp = make_request(genome_ref)
        print('-' * 80)
        print(json_resp)
        print('-' * 80)
        result = json_resp['result']
        self.assertTrue(len(result['distances']))

    def test_search_assembly(self):
        """Test a search on an Assembly type."""
        assembly_ref = '34819/10/1'
        json_resp = make_request(assembly_ref)
        print('-' * 80)
        print(json_resp)
        print('-' * 80)
        result = json_resp['result']
        self.assertTrue(len(result['distances']))

    def test_search_assembly_contigset(self):
        """Test a search on an Assembly with the legacy ContigSet."""
        assembly_ref = '34819/8/1'
        json_resp = make_request(assembly_ref)
        print('-' * 80)
        print(json_resp)
        print('-' * 80)
        result = json_resp['result']
        self.assertTrue(len(result['distances']))

    def test_search_genome_no_assembly_ref(self):
        """Test a failed search against a Genome that has no assembly_ref or contigset_ref."""
        genome_ref = '34819/5/9'
        json_resp = make_request(genome_ref)
        print('-' * 80)
        print(json_resp)
        print('-' * 80)
        self.assertTrue('no assembly or contigset references' in json_resp['error'])

    def test_search_invalid_ws_id(self):
        """Test a search with an invalid workspace reference ID."""
        ref = 'x/y/z'
        json_resp = make_request(ref)
        print('-' * 80)
        print(json_resp)
        print('-' * 80)
        self.assertTrue(len(json_resp['error']))

    def test_search_unauthorized_ws_id(self):
        """Test a search with an unauthorized workspace ref."""
        ref = '/search/1/2/3'
        json_resp = make_request(ref)
        print('-' * 80)
        print(json_resp)
        print('-' * 80)
        self.assertTrue(len(json_resp['error']))
