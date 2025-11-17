#!/usr/bin/env python3

import librovore.state as state
import librovore.xtnsmgr.configuration as config

auxdata = state.Globals()
try:
    extensions = config.extract_inventory_extensions(auxdata)
    print('Inventory extensions:', [ext.get('name') for ext in extensions])
except Exception as e:
    print('Error:', e)