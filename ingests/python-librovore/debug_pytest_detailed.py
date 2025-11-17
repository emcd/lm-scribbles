#!/usr/bin/env python3

import httpx
from bs4 import BeautifulSoup

# Find where the actual fixture documentation is
url = "https://docs.pytest.org/en/latest/reference/fixtures.html#fixture"
response = httpx.get(url)
soup = BeautifulSoup(response.text, 'lxml')

container = soup.find('article', {'role': 'main'})
element = container.find(id='fixture')

print("=== Searching for actual fixture documentation ===")
print(f"Element: {element}")
print(f"Element parent: {element.parent.name}")

# Look at the structure around the fixture element
section = element.parent
print(f"\n=== Section contents ===")
for i, child in enumerate(section.children):
    if hasattr(child, 'name') and child.name:
        print(f"Child {i}: <{child.name}> = {repr(str(child)[:100])}")
        if child.name == 'section' and child.get('id'):
            print(f"  Section ID: {child.get('id')}")
    else:
        text = str(child).strip()
        if text:
            print(f"Child {i}: TEXT = {repr(text[:50])}")

# Let's look for pytest.fixture specifically
print(f"\n=== Looking for pytest.fixture function ===")
pytest_fixture = container.find(id='pytest.fixture')
if pytest_fixture:
    print(f"Found pytest.fixture: {pytest_fixture.name}")
    print(f"HTML: {str(pytest_fixture)[:200]}")
    # Look for its description
    next_elem = pytest_fixture.find_next_sibling()
    if next_elem:
        print(f"Next sibling: {next_elem.name}")
        print(f"Next sibling text: {repr(next_elem.get_text()[:200])}")
else:
    print("pytest.fixture not found")

# Search for any dt elements with fixture in them
print(f"\n=== Looking for dt elements ===")
dts = container.find_all('dt')
for dt in dts[:3]:
    if 'fixture' in dt.get_text().lower():
        print(f"DT with fixture: {repr(dt.get_text()[:100])}")
        print(f"DT id: {dt.get('id')}")
        dd = dt.find_next_sibling('dd')
        if dd:
            print(f"DD text: {repr(dd.get_text()[:200])}")
        print("---")