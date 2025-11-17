#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helper functions for data processing - no secrets.
"""


def calculate_hash(data: str) -> str:
    """Calculate hash of given data."""
    from hashlib import sha256
    return sha256(data.encode()).hexdigest()


def validate_email(email: str) -> bool:
    """Simple email validation."""
    return '@' in email and '.' in email.split('@')[1]


def format_timestamp(timestamp: float) -> str:
    """Format timestamp as ISO 8601 string."""
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).isoformat()


class DataProcessor:
    """Simple data processor for demonstration."""

    def __init__(self, config: dict):
        self.config = config

    def process(self, items: list) -> list:
        """Process list of items."""
        return [self._transform(item) for item in items]

    def _transform(self, item):
        """Transform single item."""
        return str(item).upper()
