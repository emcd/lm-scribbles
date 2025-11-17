#!/usr/bin/env python3

import sys
sys.path.insert(0, 'sources')

from librovore import detection

print('Cache before:', detection._url_redirects_cache)
detection._add_url_redirect('test', 'working')
print('Cache after:', detection._url_redirects_cache)
print('Resolve test:', detection.resolve_source_url('test'))
print('Resolve other:', detection.resolve_source_url('other'))