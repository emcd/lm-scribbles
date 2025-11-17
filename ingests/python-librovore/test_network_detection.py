#!/usr/bin/env python3
"""Test script to detect network access during test runs."""

import pytest
import sys
import socket
import httpx
from unittest.mock import patch


def main():
    """Run tests with network instrumentation."""
    
    # Track network calls
    network_calls = []
    
    # Mock socket to detect network activity
    original_socket = socket.socket
    def instrumented_socket(*args, **kwargs):
        network_calls.append(f'socket.socket({args}, {kwargs})')
        print(f'NETWORK ACCESS: socket() called with args={args}, kwargs={kwargs}', file=sys.stderr)
        return original_socket(*args, **kwargs)
    
    # Mock httpx to detect HTTP requests
    original_get = httpx.get
    original_post = httpx.post
    original_head = httpx.head
    original_request = httpx.request
    
    def instrumented_get(*args, **kwargs):
        network_calls.append(f'httpx.get({args}, {kwargs})')
        print(f'HTTP GET: {args}, {kwargs}', file=sys.stderr)
        return original_get(*args, **kwargs)
    
    def instrumented_post(*args, **kwargs):
        network_calls.append(f'httpx.post({args}, {kwargs})')
        print(f'HTTP POST: {args}, {kwargs}', file=sys.stderr)
        return original_post(*args, **kwargs)
    
    def instrumented_head(*args, **kwargs):
        network_calls.append(f'httpx.head({args}, {kwargs})')
        print(f'HTTP HEAD: {args}, {kwargs}', file=sys.stderr)
        return original_head(*args, **kwargs)
    
    def instrumented_request(*args, **kwargs):
        network_calls.append(f'httpx.request({args}, {kwargs})')
        print(f'HTTP REQUEST: {args}, {kwargs}', file=sys.stderr)
        return original_request(*args, **kwargs)
    
    with patch('socket.socket', side_effect=instrumented_socket):
        with patch('httpx.get', side_effect=instrumented_get):
            with patch('httpx.post', side_effect=instrumented_post):
                with patch('httpx.head', side_effect=instrumented_head):
                    with patch('httpx.request', side_effect=instrumented_request):
                        exit_code = pytest.main([
                            '-x', '--tb=short', 
                            'tests/test_000_librovore/test_200_detection.py',
                            'tests/test_000_librovore/test_300_functions.py'
                        ])
    
    print(f"\nTotal network calls detected: {len(network_calls)}", file=sys.stderr)
    for call in network_calls:
        print(f"  {call}", file=sys.stderr)
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())