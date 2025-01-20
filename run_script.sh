#!/bin/bash
cd ~/Downloads/client_side
source venv/bin/activate
pip install -r requirements.txt
python create_esc.py
