#!/usr/bin/env bash

sudo fuser -k 9999/tcp
cat requirements.txt | xargs sudo apt install
python3 src/main.py
