#!/usr/bin/env python3

# Test if the configuration system picks up the MkDocs inventory processor
import os
import sys

# Add the project root to the path
project_root = "/home/me/src/python-librovore/sources"
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Try to manually run the processor registration
import librovore.state as state
import librovore.xtnsmgr.configuration as config
import librovore.xtnsmgr.processors as processors

# Create a basic globals object to test config loading
from librovore import cacheproxy
import pathlib

# Create minimal globals
auxdata = state.Globals(
    application='test',
    configuration=None,  # This will load from default location
    directories=state.DirectorySet(),
    distribution=state.DistributionDetails(),
    exits=state.ExitHandlers(),
    content_cache=cacheproxy.ContentCache(),
    probe_cache=cacheproxy.ProbeCache(),
    robots_cache=cacheproxy.RobotsCache(),
)

print("Testing configuration loading...")

try:
    inventory_extensions = config.extract_inventory_extensions(auxdata)
    print(f"Found {len(inventory_extensions)} inventory extensions:")
    for ext in inventory_extensions:
        print(f"  - {ext}")
except Exception as e:
    print(f"Error loading inventory extensions: {e}")
    import traceback
    traceback.print_exc()