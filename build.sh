#!/bin/bash
echo "Compiling C-Engine for Production..."
gcc -shared -fPIC -o ranker.so ranker.c
echo "Installing Python dependencies..."
pip install -r requirements.txt
