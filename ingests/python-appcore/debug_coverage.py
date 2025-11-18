#!/usr/bin/env python3
"""Debug why the continue statement isn't being hit."""

import sys
import os
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the sources directory to the path so we can import appcore
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'sources'))

import appcore.distribution as dist

def debug_frame_processing():
    """Debug what happens with a frame that has no __module__ or __package__."""
    
    # Create a frame with neither __module__ nor __package__
    no_info_frame = MagicMock()
    no_info_frame.f_code.co_filename = '/some/random/script.py'
    no_info_frame.f_globals = {'__module__': None, '__package__': None}
    no_info_frame.f_back = None
    
    appcore_frame = MagicMock()
    appcore_frame.f_code.co_filename = '/fake/appcore/distribution.py'
    appcore_frame.f_back = no_info_frame
    
    cwd = Path('/fake/cwd')
    
    with (
        patch('inspect.currentframe', return_value=appcore_frame),
        patch('pathlib.Path.cwd', return_value=cwd),
        patch('site.getsitepackages', return_value=['/fake/site']),
        patch('site.getusersitepackages', return_value='/fake/user/site')
    ):
        try:
            package, anchor = dist._discover_invoker_location()
            print(f"Result: package={package}, anchor={anchor}")
            print(f"Is package absent: {dist.__.is_absent(package)}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    debug_frame_processing()