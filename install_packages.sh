#!/bin/bash

# Set executable permissions for the script if not already set
if [[ ! -x "$0" ]]; then
    chmod +x "$0"
fi

# Check if a virtual environment is activated
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "Using existing virtual environment: $VIRTUAL_ENV"
else
    echo "No virtual environment found. Creating a new one..."
    python3 -m venv myenv
    source myenv/bin/activate
fi

# Install the libraries from requirements.txt
pip install -r requirements.txt

echo "Dependencies installation completed."
