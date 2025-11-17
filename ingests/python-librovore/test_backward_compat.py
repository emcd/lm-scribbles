#!/usr/bin/env python3

import librovore.cacheproxy as cp

# Test backward compatibility - should work without robots_cache parameter
cache = cp.ContentCache()
print('Backward compatibility works!')
print(f'Auto-created robots_cache: {cache.robots_cache}')

probe_cache = cp.ProbeCache()
print('ProbeCache backward compatibility works!')
print(f'Auto-created robots_cache: {probe_cache.robots_cache}')