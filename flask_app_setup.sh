#!/bin/bash

# Create base directory and subdirectories
mkdir -p app/api app/services app/models app/utils tests

# Create Python files in their respective directories
touch app/__init__.py
touch app/api/__init__.py
touch app/api/routes.py
touch app/services/data_service.py
touch app/models/user.py
touch app/utils/security.py
touch tests/__init__.py

# Create other root files
touch requirements.txt
touch Dockerfile
touch config.py

echo "Directory structure and files created successfully."
