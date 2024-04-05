import unittest
from django.test import TestCase, Client


class ApiTests(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.client = Client()

    def test_api_response(self):
        response = self.client.get('/api/files')
        for element in response.json()['files']:
            self.assertIsInstance(element, str)
        self.assertEqual(response.status_code, 200)
