from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
import os
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer

from apis.models import FileSampleData

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = os.path.join(BASE_DIR, 'Data')


class FileListView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        file_info = []
        for filename in os.listdir(DATA_DIR):
            filepath = os.path.join(DATA_DIR, filename)
            try:
                file_info.append(filename)

            except Exception as e:
                file_info.append({'filename': filename, 'error': str(e)})

        return JsonResponse({'files': file_info})

    def put(self, request):
        print(request.data)
        try:
            file = request.data.getlist('files[]')[0]
            print(file)
            file_name = file.name
            filepath = os.path.join(BASE_DIR, 'Data', file_name)

            with open(filepath, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            return JsonResponse({'message': 'File uploaded successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)})

    def post(self, request, *args, **kwargs):
        file_name = request.data.get('file_name', None)
        if not file_name:
            return JsonResponse({'error': 'Missing file_name parameter'}, status=400)

        try:
            data_entry = FileSampleData.objects.get(filename=file_name)
            return JsonResponse(data_entry.data_dict, status=200)

        except FileSampleData.DoesNotExist:
            data_path = os.path.join(DATA_DIR, file_name)
        try:
            df = pd.read_csv(data_path)
            imputer = SimpleImputer(strategy='most_frequent')
            df = pd.DataFrame(imputer.fit_transform(df))
            response_data = {}
            for col in df.columns:
                response_data[col] = df[col].to_list()[:5]

            # Save to database
            data_entry = FileSampleData(filename=file_name, data_dict=response_data)
            data_entry.save()
            return JsonResponse(response_data, status=200)

        except FileNotFoundError:
            return JsonResponse({'error': f'File not found: {file_name}'}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
