#!/usr/bin/env python3
''' Test script for parsing token usage from conversation transcript. '''

import json
from pathlib import Path

# Our current session transcript
transcript_path = Path.home() / '.config/claude/projects/-home-me-src-agents-common/72687e8f-409b-4c1d-81e2-8bedbfa401f3.jsonl'

print( f"Reading transcript: {transcript_path}" )
print( )

# Read last N lines of JSONL (more efficient than reading entire file)
with open( transcript_path, 'rb' ) as f:
    # Seek to near end, read last chunk
    f.seek( 0, 2 )  # End of file
    size = f.tell( )
    chunk_size = 10000
    f.seek( max( 0, size - chunk_size ) )
    lines = f.read( ).decode( 'utf-8' ).splitlines( )

print( f"Read last {len( lines )} lines from transcript" )
print( )

# Find most recent assistant message with usage data
for line in reversed( lines ):
    if not line.strip( ):
        continue
    try:
        msg = json.loads( line )
        if msg.get( 'type' ) == 'assistant' and 'message' in msg:
            usage = msg[ 'message' ].get( 'usage' )
            if usage:
                # Show all token types
                input_tokens = usage.get( 'input_tokens', 0 )
                cache_creation = usage.get( 'cache_creation_input_tokens', 0 )
                cache_read = usage.get( 'cache_read_input_tokens', 0 )
                output_tokens = usage.get( 'output_tokens', 0 )

                print( "Most recent usage data:" )
                print( f"  input_tokens: {input_tokens:,}" )
                print( f"  cache_creation_input_tokens: {cache_creation:,}" )
                print( f"  cache_read_input_tokens: {cache_read:,}" )
                print( f"  output_tokens: {output_tokens:,}" )
                print( )

                # Calculate total
                total = input_tokens + cache_creation + cache_read + output_tokens
                print( f"Total tokens: {total:,}" )
                print( f"Formatted: {total:,}/200,000" )

                # Also show percentage
                percentage = ( total / 200000 ) * 100
                print( f"Usage: {percentage:.1f}%" )

                break
    except json.JSONDecodeError:
        continue
else:
    print( "No usage data found in transcript" )
