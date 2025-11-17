#!/usr/bin/env python3

import httpx
from bs4 import BeautifulSoup

# Look for the actual @pytest.fixture function
url = "https://docs.pytest.org/en/latest/reference/fixtures.html"
response = httpx.get(url)
soup = BeautifulSoup(response.text, 'lxml')

container = soup.find('article', {'role': 'main'})

print("=== Looking for pytest.fixture decorator function ===")
# Search for dt elements that might contain the fixture decorator
dts = container.find_all('dt')
print(f"Found {len(dts)} dt elements")

for i, dt in enumerate(dts):
    dt_text = dt.get_text()
    if 'pytest.fixture' in dt_text or '@fixture' in dt_text:
        print(f"\n=== DT {i} with fixture ===")
        print(f"DT text: {repr(dt_text[:150])}")
        print(f"DT id: {dt.get('id')}")
        
        # Look for description in next sibling
        dd = dt.find_next_sibling('dd')
        if dd:
            dd_text = dd.get_text()
            print(f"DD text (first 200): {repr(dd_text[:200])}")
        else:
            print("No DD sibling found")

# Also search for any element with id containing pytest.fixture
print(f"\n=== Searching for elements with pytest.fixture in id ===")
for elem in container.find_all(id=lambda x: x and 'pytest.fixture' in x):
    print(f"Found element: {elem.name} with id='{elem.get('id')}'")
    print(f"Text: {repr(elem.get_text()[:100])}")

# Let's also try searching by text content
print(f"\n=== Searching for '@pytest.fixture' in text ===")
for elem in container.find_all(text=lambda text: text and '@pytest.fixture' in text):
    parent = elem.parent
    print(f"Found text in {parent.name}: {repr(str(elem)[:100])}")
    if parent.get('id'):
        print(f"Parent id: {parent.get('id')}")