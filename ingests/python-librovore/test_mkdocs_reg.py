#!/usr/bin/env python3

import librovore.inventories.mkdocs
import librovore.processors

print('Before registration:', list(librovore.processors.inventory_processors.keys()))
librovore.inventories.mkdocs.register({})
print('After registration:', list(librovore.processors.inventory_processors.keys()))