#!/bin/bash

# Exit immediately if any command fails
set -e

# Get the directory of the config.sh
SCRIPT_DIR=$(dirname "$0")

# Change to the directory of the script
cd "$SCRIPT_DIR"

# Activate the Python virtual environment
source venv/bin/activate

# Run the extractor so we have the data of each book
echo "Running src/extractor/main.py..."
python3 src/extractor/main.py

# If the first script was successful, run the creation of the vector database index
echo "Running src/vdb_generator/main.py..."
python3 src/vdb_generator/main.py

echo "Scripts executed successfully. Configuration done!"

# Deactivate the virtual environment
deactivate