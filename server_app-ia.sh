#!/bin/bash
source "$HOME/miniforge3/bin/activate" facegate
cd "$HOME/facegate/app-ia"

# Intenta matar instancias anteriores sin fallar si no existen
pkill -f "python run.py" || true

# Inicia la app
python run.py
