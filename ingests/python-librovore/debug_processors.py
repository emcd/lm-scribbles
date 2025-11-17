#!/usr/bin/env python3

import librovore.processors as proc_mod
print('Initial inventory processors:', list(proc_mod.inventory_processors.keys()))

# Try to manually import and register MkDocs
try:
    import librovore.inventories.mkdocs
    librovore.inventories.mkdocs.register({})
    print('After manual MkDocs registration:', list(proc_mod.inventory_processors.keys()))
except Exception as e:
    print('Error during manual registration:', e)