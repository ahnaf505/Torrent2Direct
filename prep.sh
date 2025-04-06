#!/bin/bash

if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install it first."
    exit 1
fi

if ! command -v pip &> /dev/null; then
    echo "pip is not installed. Installing pip..."
    sudo apt update -qq && sudo apt install -y -qq python3-pip
fi

echo "Installing required Python packages..."
pip install --quiet -r requirements.txt

if ! command -v patchelf &> /dev/null; then
    echo "Installing patchelf..."
    sudo apt update -qq && sudo apt install -y -qq patchelf
fi

if [ ! -d "temp" ]; then
    echo "Creating 'temp' directory..."
    mkdir temp
fi

if [ ! -f "links.txt" ]; then
    echo "Creating 'links.txt' file..."
    touch links.txt
fi

echo "Preparation completed. You can now run the main script."