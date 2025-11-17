#!/usr/bin/env python3

from librovore.inventories.mkdocs import __
from librovore.inventories.mkdocs.main import MkDocsInventoryProcessor

print('Before registration:', list(__.inventory_processors.keys()))
processor = MkDocsInventoryProcessor()
__.inventory_processors['mkdocs'] = processor
print('After registration:', list(__.inventory_processors.keys()))