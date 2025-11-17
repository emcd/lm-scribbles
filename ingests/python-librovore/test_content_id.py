#!/usr/bin/env python3

from librovore.results import parse_content_id

# Test the parsing function
content_id = 'aHR0cHM6Ly9kb2NzLnB5dGhvbi5vcmcvMzpwYXRobGli'
result = parse_content_id(content_id)
print('Location:', repr(result[0]))
print('Object name:', repr(result[1]))
print('Full result:', result)