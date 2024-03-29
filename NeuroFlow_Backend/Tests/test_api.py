import unittest
from django.test import TestCase, Client


class ApiTests(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.client = Client()

    def test_api_response(self):
        response = self.client.get('/api/files/')
        for element in response.json()['files']:
            self.assertIn('filename', element)  # Check if 'filename' exists
            self.assertIn('columns', element)  # Check if 'columns' exists
            self.assertIsInstance(element['columns'], list)  # Check if 'columns' is a list
            columns = element['columns']
            for column in columns:
                self.assertIsInstance(column, str)  # Check if each column is a string
        self.assertEqual(response.status_code, 200)
