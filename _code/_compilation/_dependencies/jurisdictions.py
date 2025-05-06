#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load WCPD jurisdictions from a JSON file.
"""

import json
import os

# Define path to the JSON file
json_path = os.path.join(os.path.dirname(__file__), "jurisdictions.json")

# Load jurisdictions dictionary from file
with open(json_path, 'r', encoding='utf-8') as f:
    jurisdictions = json.load(f)
