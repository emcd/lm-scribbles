#!/usr/bin/env python3
"""Test file for experimenting with line-based editing."""

def renamed_function():
    """This function has been renamed and updated."""
    print("Hello, world!")
    return "renamed_and_updated"

class TestClass:
    """A test class with multiple methods."""
    
    def method_one(self):
        """First method."""
        return 1
    
    def method_two(self):
        """Second method."""
        return 2

# Some variables
new_variable = "new_value"
another_variable = 42

# Function with similar content that might confuse context-based editing
def similar_function():
    """This is a similar function."""
    print("Hello, world!")  # Same line as original_function
    return "similar"

if __name__ == "__main__":
    print("Running test file")
    result = original_function()
    print(f"Result: {result}")