import requests
import unittest
import json
import re

class PySearchTests(unittest.TestCase):

    def setUp(self):
        self.elastic_url = 'http://localhost:9200/'

    def test_elastic_search_server_is_on(self):
        r = requests.get(self.elastic_url)
        self.assertEqual(r.status_code, 200)

    def test_doc_can_be_found(self):

        url = self.elastic_url + '/job/all/_search?pretty=1'

        doc = {
            'query': {
                'prefix':
                    {'description.suggestions':'job'}
            },
            'facets': {
                'description_suggestions':
                    { 'terms':
                          { 'field':'description.suggestions','regex':'Title.*|^job.*', 'size': 10 }
                    }
            }
        }

        data = json.dumps(doc)
        r = requests.get(url, data=data)
        result = r.text
        print result
        self.assertEqual(r.status_code, 200)