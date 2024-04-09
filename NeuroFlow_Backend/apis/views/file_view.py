from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
import os
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer

from apis.models import FileData

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
            data_entry = FileData.objects.get(filename=file_name)
            return JsonResponse(data_entry.data_dict, status=200)

        except FileData.DoesNotExist:
            data_path = os.path.join(DATA_DIR, file_name)
        try:
            df = pd.read_csv(data_path)
            imputer = SimpleImputer(strategy='most_frequent')
            df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

            sample_data = df.head(10).to_dict('list')
            column_sums = {}
            for column in df.columns:
                unique_counts = df[column].value_counts()
                if unique_counts.size < 10:
                    column_sums[column] = {
                        'categories': list(unique_counts.index),
                        'values': [int(x) for x in unique_counts.values] # Convert to int
                    }

            # FileData(filename=file_name, data_dict=sample_data).save()  # save to database
            return JsonResponse({
                "sample_data": sample_data,
                "column_sum_data": column_sums
            }, status=200)

        except FileNotFoundError:
            return JsonResponse({'error': f'File not found: {file_name}'}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
