#!/usr/bin/env python3

import sphinxmcps.functions as f
import sphinxmcps.interfaces as i

print('Functions module imports successfully')
print('SearchBehaviors:', i.SearchBehaviors())
print('Default filters:', f._filters_default)
print('Default search behaviors:', f._search_behaviors_default)

# Test that the new architecture works
sb = i.SearchBehaviors(match_mode=i.MatchMode.Fuzzy, fuzzy_threshold=75)
filters = {'domain': 'py', 'role': 'function'}
print('Sample SearchBehaviors:', sb)
print('Sample filters:', filters)