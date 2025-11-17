#!/usr/bin/env python3

import sys
sys.path.insert(0, '.')
from sources.librovore.functions import normalize_location

# Safe cases that should be normalized
print('Safe: https://docs.python.org/3/library/index.html ->', normalize_location('https://docs.python.org/3/library/index.html'))
print('Safe: https://fastapi.tiangolo.com/tutorial/index.html ->', normalize_location('https://fastapi.tiangolo.com/tutorial/index.html'))

# Cases that should NOT be normalized (preserved)
print('Preserve: https://docs.python.org/3/library/ ->', normalize_location('https://docs.python.org/3/library/'))
print('Preserve: file:///path/index.html ->', normalize_location('file:///path/index.html'))
print('Preserve: docs/jsindex.html ->', normalize_location('docs/jsindex.html'))
print('Preserve: myindex.html ->', normalize_location('myindex.html'))