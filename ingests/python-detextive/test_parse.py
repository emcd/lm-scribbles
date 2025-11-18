import detextive

result = detextive.inference.parse_http_content_type('   ')
print(f'Result: {result}')
print(f'First is absent: {detextive.__.is_absent(result[0])}')
print(f'First value: {repr(result[0])}')

# Test what is_textual_mimetype does with empty string
print(f'is_textual_mimetype(""): {detextive.mimetypes.is_textual_mimetype("")}')