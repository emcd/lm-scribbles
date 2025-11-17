#!/usr/bin/env python3

def test_truncation_logic():
    """Test the CLI truncation logic with sample content."""
    
    # Simulate the markdown content from markdownify
    description = '''Usage Documentation

[Models](../../concepts/models/)

A base class for creating Pydantic models.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `__class_vars__` | `set[str]` | The names of the class variables defined on the model. |
| `__private_attributes__` | `Dict[str, ModelPrivateAttr]` | Metadata about the private attributes of the model. |'''
    
    print(f"Original description length: {len(description)}")
    print(f"Original line count: {len(description.split(chr(10)))}")
    
    # Test truncation logic
    lines_max = 40
    lines = description.split('\n')
    print(f"Number of lines: {len(lines)}")
    
    if len(lines) > lines_max:
        truncated_lines = lines[:lines_max]
        truncated_lines.append('...')
        truncated_description = '\n'.join(truncated_lines)
    else:
        truncated_description = description
    
    print(f"Truncated description:")
    print(repr(truncated_description))
    
    print(f"\nFirst few lines:")
    for i, line in enumerate(lines[:5]):
        print(f"{i+1}: {repr(line)}")

if __name__ == "__main__":
    test_truncation_logic()