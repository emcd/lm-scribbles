#!/usr/bin/env python3

import toml
config_path = "/home/me/src/python-librovore/data/configuration/general.toml"

with open(config_path, 'r') as f:
    config = toml.load(f)

print("Inventory extensions in config:")
for ext in config.get('inventory-extensions', []):
    print(f"  - Name: {ext.get('name')}, Enabled: {ext.get('enabled', True)}")