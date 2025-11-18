from pathlib import Path
import sys
sys.path.insert(0, 'sources')
from agentsmgr.commands import base, generator, operations

target = Path('.auxiliary/scribbles/populate-test').resolve()
source = 'defaults'

location = base.retrieve_data_location(source)
print(f'Data location: {location}')

# Try to load configuration
import asyncio
async def test():
    config = await base.retrieve_configuration(target)
    print(f'Configuration: {config}')
    gen = generator.ContentGenerator(location=location, configuration=config)

    # Try to populate
    items_attempted, items_written = operations.populate_directory(gen, target, simulate=False)
    print(f'Attempted: {items_attempted}, Written: {items_written}')

    # Check if files were created
    commands_dir = target / '.auxiliary' / 'configuration' / 'claude' / 'commands'
    if commands_dir.exists():
        files = list(commands_dir.glob('*.md'))
        print(f'Created {len(files)} command files')
        for f in files[:3]:
            print(f'  - {f.name}')

asyncio.run(test())
