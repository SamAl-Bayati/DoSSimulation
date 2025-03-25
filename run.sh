#!/usr/bin/env bash

# Kill any process using port 9999 (if exists)
sudo fuser -k 9999/tcp

# Install dependencies
cat requirements.txt | xargs sudo apt install

# Start the main application
python3 src/main.py
