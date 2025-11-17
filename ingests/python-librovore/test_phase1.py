#!/usr/bin/env python3

import librovore.cacheproxy as cp
import librovore.state as state
import appcore

class MockGlobals(appcore.Globals):
    def __init__(self):
        self.configuration = {}

auxdata = MockGlobals()
content_cache, probe_cache, robots_cache = cp.prepare(auxdata)
print('Phase 1 basic functionality works!')
print(f'content_cache.robots_cache: {content_cache.robots_cache}')
print(f'probe_cache.robots_cache: {probe_cache.robots_cache}')  
print(f'Same robots_cache shared: {content_cache.robots_cache is probe_cache.robots_cache}')
print(f'Both point to returned robots_cache: {content_cache.robots_cache is robots_cache}')