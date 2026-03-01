#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Verifying installation..."
python -c "import flask; import pandas; import numpy; import boto3; print('All packages installed successfully')"

echo "Build complete!"
