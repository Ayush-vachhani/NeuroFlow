from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
import os
from pathlib import Path
import pandas as pd
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = os.path.join(BASE_DIR, 'Data')


class FileListView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        file_info = []
        for filename in os.listdir(DATA_DIR):
            filepath = os.path.join(DATA_DIR, filename)
            try:
                df = pd.read_csv(filepath)
                file_info.append({
                    'filename': filename,
                    'columns': df.columns.tolist(),
                })
            except Exception as e:
                file_info.append({'filename': filename, 'error': str(e)})

        return JsonResponse({'files': file_info})
