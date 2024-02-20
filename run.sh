#!/bin/bash

# Starting Backend
echo "Starting Backend..."
gnome-terminal -- bash -c "cd NeuroFlow_Backend; source .venv/bin/activate; python manage.py runserver; exec bash"

# Starting UI
echo "Starting UI..."
gnome-terminal -- bash -c "cd UI; pnpm run dev; exec bash"

echo "Servers are starting..."
