#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Verifying gunicorn installation..."
which gunicorn
gunicorn --version

echo "Build complete!"
