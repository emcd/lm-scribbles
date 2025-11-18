import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / 'sources'))

from agentsmgr.commands import ContentGenerator, generate_items_to_directory
import yaml

# Load configuration
with open('data/agentsmgr/profiles/answers-default.yaml') as f:
    config = yaml.safe_load(f)

# Create generator
location = Path('defaults').resolve()
print(f'Location: {location}')
print(f'Exists: {location.exists()}')

try:
    generator = ContentGenerator(location=location, configuration=config)
    print(f'Generator created successfully')

    # Try to generate to a temp directory
    import tempfile
    temp_dir = Path(tempfile.mkdtemp())
    print(f'Temp dir: {temp_dir}')

    attempted, written = generate_items_to_directory(generator, temp_dir, simulate=False)
    print(f'Generated: {attempted} attempted, {written} written')

    # Check what was created
    import subprocess
    subprocess.run(['tree', str(temp_dir)])
except Exception as e:
    print(f'Error: {type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()
