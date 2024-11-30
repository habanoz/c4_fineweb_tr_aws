#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: Bucket name is not set"
  exit 1
fi

echo "Installing packages"
sudo apt update
sudo apt install build-essential -qq  -y
sudo apt install python3.12-dev -qq -y
sudo apt install python3.12-venv -qq -y

echo "Creating venv"
python3 -m venv .venv
source .venv/bin/activate

echo "Installing dependencies"
pip3 install -q -r requirements.txt

echo "Running script"
huggingface-cli login --token "$2"
export HF_HUB_ENABLE_HF_TRANSFER=1
python3 hf_writer.py -ts 1024 -w 1 --random_start 0 "s3://$1/tokenize-dir-1024/base_processing/output" "s3://$1/tokenize-dir-1024" habanoz/c4_tr_fineweb

echo "Done!"