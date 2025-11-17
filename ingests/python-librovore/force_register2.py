#!/usr/bin/env python3

# Force register using direct imports
import sys
import importlib

# Direct import the module
mkdocs_mod = importlib.import_module('librovore.inventories.mkdocs')
processors_mod = importlib.import_module('librovore.processors')

print("Before registration:", list(processors_mod.inventory_processors.keys()))
mkdocs_mod.register({})
print("After registration:", list(processors_mod.inventory_processors.keys()))