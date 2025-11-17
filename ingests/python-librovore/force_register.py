#!/usr/bin/env python3

# Force register the MkDocs inventory processor and test it
import librovore.inventories.mkdocs
import librovore.processors

# Force registration
print("Forcing MkDocs inventory processor registration...")
librovore.inventories.mkdocs.register({})

# Verify registration
print("Registered inventory processors:", list(librovore.processors.inventory_processors.keys()))

# Test with HTTPX
import asyncio
import librovore.detection
import librovore.state

async def test_httpx():
    # Create minimal state
    auxdata = librovore.state.Globals(
        application='test',
        configuration=None,
        directories=librovore.state.DirectorySet(),
        distribution=librovore.state.DistributionDetails(),
        exits=librovore.state.ExitHandlers(),
        content_cache=librovore.cacheproxy.ContentCache(),
        probe_cache=librovore.cacheproxy.ProbeCache(),
        robots_cache=librovore.cacheproxy.RobotsCache(),
    )
    
    try:
        detection = await librovore.detection.detect_inventory(auxdata, "https://www.python-httpx.org/")
        print(f"Detection successful! Processor: {detection.processor.name}, Confidence: {detection.confidence}")
    except Exception as e:
        print(f"Detection failed: {e}")

# Note: this won't work due to globals creation issues, but shows the concept
print("Test concept ready - would test HTTPX detection here")