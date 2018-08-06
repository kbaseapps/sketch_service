"""
Simple integration tests on the API itself.

We make actual ajax requests to the running docker container.
"""

import unittest
import requests

# This must be the URL of the running server from within the docker container
url = 'http://0.0.0.0:5000/'


class TestApi(unittest.TestCase):

    def test_root(self):
        """Test the root endpoint."""
        resp = requests.get(url)
        # Don't particularly feel the need to test the content of this
        self.assertTrue(len(resp.text))
