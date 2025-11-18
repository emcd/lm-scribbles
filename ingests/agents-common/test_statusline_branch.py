#!/usr/bin/env python3
''' Quick test of Git branch detection. '''

import sys
sys.path.insert( 0, '/home/me/.config/claude' )

from statusline import _detect_git_branch

# Test in current Git repo
branch = _detect_git_branch( '/home/me/src/agents-common' )
print( f"Current branch: {branch}" )

# Test in non-Git directory
branch_none = _detect_git_branch( '/tmp' )
print( f"Non-git directory: {branch_none}" )

# Test with home directory shorthand
branch_home = _detect_git_branch( '~' )
print( f"Home directory: {branch_home}" )
