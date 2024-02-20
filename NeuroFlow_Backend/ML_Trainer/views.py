from pathlib import Path
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response

BASE_DIR = Path(__file__).resolve().parent.parent


class CSVColumnsView(APIView):
    @classmethod
    def get(cls, request):
        try:
            # Load the CSV file
            df = pd.read_csv('Data/Titanic/train.csv')
            # Get the columns as a list
            columns = df.columns.tolist()
            # Directly return the data as a response
            return Response({"columns": columns})
        except FileNotFoundError:
            return Response({"error": "File not found"}, status=404)
