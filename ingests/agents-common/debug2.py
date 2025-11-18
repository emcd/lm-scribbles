from pathlib import Path
location = Path('.').resolve()
item_type = 'commands'
coder = 'claude'
item_name = 'cs-annotate-release'

primary_path = location / "defaults" / "contents" / item_type / coder / f"{item_name}.md"
print(f'Looking for: {primary_path}')
print(f'Exists: {primary_path.exists()}')
print(f'Actual path should be: defaults/contents/commands/claude/cs-annotate-release.md')

# What the code actually does
primary_path2 = location / "contents" / item_type / coder / f"{item_name}.md"
print(f'Code is looking for: {primary_path2}')
print(f'Exists: {primary_path2.exists()}')
