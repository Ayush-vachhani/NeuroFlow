import csv
from django.shortcuts import render
import os.path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def index(request):
    file_path = 'Data/Titanic/train.csv'  # Update this to your CSV file path
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        columns = next(reader)  # This reads the first line which is typically the header

    return render(request, 'index.html', {'columns': columns})
