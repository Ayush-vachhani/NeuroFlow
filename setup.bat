@echo off
SETLOCAL EnableDelayedExpansion

:: Install pnpm globally if it's not already installed
npm list -g pnpm || npm install -g pnpm

:: Change to UI directory and install dependencies
cd "UI"
pnpm i
cd ..

:: Change to NeuroFlow_Backend directory
cd "NeuroFlow_Backend"

:: Activate virtual environment and install Python dependencies
:: Assuming the venv is named .venv
CALL .venv\Scripts\activate.bat
pip install -r requirements.txt

CALL .venv\Scripts\deactivate.bat

echo Setup completed.