from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
import os
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
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
        file_name = request.data.get('file_name')
        if not file_name:
            return JsonResponse({'error': 'Missing file_name parameter'}, status=400)

        data_path = os.path.join(DATA_DIR, file_name)
        try:
            print("Trying to read file")
            df = pd.read_csv(data_path)
            target_column = df.columns[-1]
            features = df.drop(target_column, axis=1)
            for col in df.columns:
                if df[col].dtype == 'object':
                    num_unique_values = df[col].nunique()
                    if num_unique_values <= 10:
                        encoder = LabelEncoder()
                        df[col] = encoder.fit_transform(df[col])
                    else:
                        print(f"dropping column {col}")
                        df.drop(col, axis=1, inplace=True)
            df.info()
            print("Info infered")
            correlations = features.corr()
            print("correlations set")
            return JsonResponse({'correlations': correlations.to_dict()}, status=200)

        except FileNotFoundError:
            return JsonResponse({'error': f'File not found: {file_name}'}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
