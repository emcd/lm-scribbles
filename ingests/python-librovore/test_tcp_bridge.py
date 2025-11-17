#!/usr/bin/env python3
"""
Simple test script to verify TCP bridging functionality.
"""

import asyncio
import sys
import subprocess
import time
import socket

async def test_tcp_bridge():
    """Test the TCP bridging functionality."""
    port = 8007
    
    # Start the TCP bridge server
    print(f"Starting TCP bridge on port {port}...")
    server_process = await asyncio.create_subprocess_exec(
        'hatch', 'run', 'sphinxmcps', 'serve', '--port', str(port),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    # Wait a moment for server to start and check output
    await asyncio.sleep(2)
    
    # Check if server started successfully
    if server_process.returncode is not None:
        stdout, stderr = await server_process.communicate()
        print(f"Server failed to start. Exit code: {server_process.returncode}")
        print(f"Stdout: {stdout.decode()}")
        print(f"Stderr: {stderr.decode()}")
        return
    
    try:
        # Connect and test MCP protocol
        print("Connecting to TCP bridge...")
        reader, writer = await asyncio.open_connection('localhost', port)
        
        # Send initialize request
        init_request = '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"roots":{"listChanged":true},"sampling":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}},"id":1}\n'
        
        print("Sending initialize request...")
        writer.write(init_request.encode())
        await writer.drain()
        
        # Read response
        response = await reader.readline()
        print(f"Response: {response.decode().strip()}")
        
        # Close connection
        writer.close()
        await writer.wait_closed()
        
        print("✅ TCP bridge test successful!")
        
    except Exception as e:
        print(f"❌ TCP bridge test failed: {e}")
    finally:
        # Cleanup server and all child processes
        try:
            # First try graceful termination
            server_process.terminate()
            await asyncio.wait_for(server_process.wait(), timeout=3.0)
        except asyncio.TimeoutError:
            # Force kill if graceful termination fails
            server_process.kill()
            await server_process.wait()
        
        # Also cleanup any orphaned hatch processes on the port
        try:
            cleanup_process = await asyncio.create_subprocess_exec(
                'pkill', '-f', f'serve --port {port}',
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            await cleanup_process.wait()
        except Exception:
            pass  # Cleanup is best-effort

if __name__ == "__main__":
    asyncio.run(test_tcp_bridge())