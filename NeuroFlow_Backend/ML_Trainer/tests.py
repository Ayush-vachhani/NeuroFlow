from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import pandas as pd


class CSVColumnsViewTest(APITestCase):

    def setUp(self):
        # Setup run before every test method.
        pass

    def test_get_csv_columns_success(self):
        # Assume 'csv_columns_url' is the name you've given to the URL of CSVColumnsView in your urls.py
        url = reverse('csv_columns')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_columns = pd.read_csv('Data/Titanic/train.csv').columns.tolist()
        self.assertEqual(response.data["columns"], expected_columns)

    def test_csv_file_not_found(self):
        pass
