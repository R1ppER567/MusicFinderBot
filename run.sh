#!/bin/bash

set -e

if [[ -d "venv" ]]; then
    source venv/bin/activate
elif [[ -d ".venv" ]]; then
    source .venv/bin/activate
else
    echo "Error: Virtual environment not found!"
    exit 1
fi

python3 bot.py
