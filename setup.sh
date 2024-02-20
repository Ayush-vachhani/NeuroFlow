#!/bin/bash

# Check if pnpm is installed; if not, install it globally
if ! command -v pnpm &> /dev/null
then
    echo "pnpm could not be found, installing it globally..."
    npm install -g pnpm
fi

# Change to UI directory and install dependencies
cd "UI" || exit
pnpm i
cd ..

# Change to NeuroFlow_Backend directory
cd "NeuroFlow_Backend" || exit

# Activate virtual environment and install Python dependencies
# Assuming the venv is located at .venv
source .venv/bin/activate
pip install -r requirements.txt

# Deactivate virtual environment
deactivate

echo "Setup completed."
