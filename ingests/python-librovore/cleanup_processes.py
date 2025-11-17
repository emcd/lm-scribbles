#!/usr/bin/env python3
"""
Utility to cleanup leaked MCP server processes.
"""

import subprocess
import sys

def cleanup_mcp_processes():
    """Find and kill leaked MCP server processes."""
    try:
        # Find all processes matching our pattern
        result = subprocess.run(
            ['pgrep', '-f', 'sphinxmcps serve --port'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            print(f"Found {len(pids)} MCP server processes to cleanup:")
            
            for pid in pids:
                if pid:
                    try:
                        # Get process info
                        info_result = subprocess.run(
                            ['ps', '-p', pid, '-o', 'pid,cmd'],
                            capture_output=True,
                            text=True
                        )
                        lines = info_result.stdout.split('\n')
                        cmd_info = lines[1] if info_result.returncode == 0 and len(lines) > 1 else 'Unknown'
                        print(f"  PID {pid}: {cmd_info}")
                        
                        # Kill the process
                        subprocess.run(['kill', pid], check=True)
                        print(f"  ✅ Killed PID {pid}")
                        
                    except subprocess.CalledProcessError:
                        print(f"  ⚠️  Could not kill PID {pid} (may already be dead)")
                        
        else:
            print("✅ No leaked MCP server processes found")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during cleanup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    cleanup_mcp_processes()
    print("🧹 Cleanup complete!")