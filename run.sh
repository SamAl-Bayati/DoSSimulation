#!/usr/bin/env bash

# Install dependencies
cat requirements.txt | xargs sudo apt install

# 2. Start the main application
python3 src/main.py
