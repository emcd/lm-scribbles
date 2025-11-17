#!/usr/bin/env python3

import sys
sys.path.insert(0, '.')
from sources.librovore.functions import normalize_location

print('Test 1:', normalize_location('https://docs.python.org/3/library/index.html'))
print('Test 2:', normalize_location('https://fastapi.tiangolo.com/tutorial/index.html'))
print('Test 3:', normalize_location('https://docs.python.org/3/library/'))
print('Test 4:', normalize_location('file:///path/index.html'))
print('Test 5:', normalize_location('docs/index.html'))