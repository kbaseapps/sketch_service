"""
Simple integration tests on the API itself.

We make actual ajax requests to the running docker container.
"""

import unittest
import requests

# This must be the URL of the running server from within the docker container
url = 'http://0.0.0.0:5000'


class TestApi(unittest.TestCase):

    def test_root(self):
        """Test the root endpoint."""
        resp = requests.get(url)
        # Don't particularly feel the need to test the content of this
        self.assertTrue(len(resp.text))

    def test_search_reads_paired(self):
        """Test a search on genome read data with paired-ends."""
        reads_ref = '15/45/1'
        full_url = url + '/search/' + reads_ref
        resp = requests.get(full_url)
        json = resp.json()
        self.assertTrue(len(json['distances']))

    def test_search_reads_single(self):
        """Test a search on single-ended genome read data."""
        reads_ref = '15/43/1'
        full_url = url + '/search/' + reads_ref
        resp = requests.get(full_url)
        json = resp.json()
        self.assertTrue(len(json['distances']))

    def test_search_genome(self):
        """Test a search on a Genome type."""
        genome_ref = '34819/14/1'
        full_url = url + '/search/' + genome_ref
        resp = requests.get(full_url)
        json = resp.json()
        self.assertTrue(len(json['distances']))

    def test_search_assembly(self):
        """Test a search on an Assembly type."""
        assembly_ref = '34819/10/1'
        full_url = url + '/search/' + assembly_ref
        resp = requests.get(full_url)
        json = resp.json()
        self.assertTrue(len(json['distances']))

    def test_search_assembly_contigset(self):
        """Test a search on an Assembly with the legacy ContigSet."""
        assembly_ref = '34819/8/1'
        full_url = url + '/search/' + assembly_ref
        resp = requests.get(full_url)
        json = resp.json()
        self.assertTrue(len(json['distances']))

    def test_search_genome_no_assembly_ref(self):
        """Test a failed search against a Genome that has no assembly_ref or contigset_ref."""
        genome_ref = '34819/5/9'
        full_url = url + '/search/' + genome_ref
        resp = requests.get(full_url)
        json = resp.json()
        self.assertEqual(json['status'], 'error')
        self.assertTrue('no assembly or contigset references' in json['message'])

    def test_search_invalid_ws_id(self):
        """Test a search with an invalid workspace reference ID."""
        full_url = url + '/search/x/y/z'
        resp = requests.get(full_url)
        json = resp.json()
        self.assertEqual(json['status'], 'error')
        self.assertTrue(len(json['message']))

    def test_search_unauthorized_ws_id(self):
        """Test a search with an unauthorized workspace ref."""
        full_url = url + '/search/1/2/3'
        resp = requests.get(full_url)
        json = resp.json()
        self.assertEqual(json['status'], 'error')
        self.assertTrue(len(json['message']))
