#!/usr/bin/env python3
"""
Test script for the new stdio-over-tcp transport with dynamic port assignment.
"""

import asyncio
import json
import sys
import signal
import os

async def test_stdio_over_tcp():
    """Test the stdio-over-tcp transport functionality."""
    
    # Test dynamic port assignment (port 0)
    print("Testing stdio-over-tcp with dynamic port assignment...")
    server_process = await asyncio.create_subprocess_exec(
        'hatch', 'run', 'sphinxmcps', 'serve', 
        '--transport', 'stdio-over-tcp', '--port', '0',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        preexec_fn=os.setsid  # Create new process group
    )
    
    # Wait for server to start and capture dynamic port
    await asyncio.sleep(2)
    
    # Check if server started successfully
    if server_process.returncode is not None:
        stdout, stderr = await server_process.communicate()
        print(f"Server failed to start. Exit code: {server_process.returncode}")
        print(f"Stdout: {stdout.decode()}")
        print(f"Stderr: {stderr.decode()}")
        return
    
    # Parse stderr to get the dynamic port
    stderr_data = await asyncio.wait_for(
        server_process.stderr.read(1024), timeout=1
    )
    stderr_text = stderr_data.decode()
    print(f"Server output: {stderr_text}")
    
    # Extract port from output like "Serving MCP stdio over TCP on 127.0.0.1:54321"
    import re
    port_match = re.search(r'127\.0\.0\.1:(\d+)', stderr_text)
    if not port_match:
        print("❌ Could not find dynamic port in server output")
        await cleanup_server(server_process)
        return
    
    dynamic_port = int(port_match.group(1))
    print(f"✅ Server started on dynamic port: {dynamic_port}")
    
    try:
        # Connect and test MCP protocol
        print("Connecting to stdio-over-tcp server...")
        reader, writer = await asyncio.open_connection('localhost', dynamic_port)
        
        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "method": "initialize", 
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"roots": {"listChanged": True}, "sampling": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            },
            "id": 1
        }
        
        request_line = json.dumps(init_request) + '\n'
        writer.write(request_line.encode())
        await writer.drain()
        
        # Read response
        response_line = await reader.readline()
        response = json.loads(response_line.decode().strip())
        
        print(f"✅ Initialize response: {response['result']['serverInfo']['name']}")
        
        # Send initialized notification (required after initialize)
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        
        request_line = json.dumps(initialized_notification) + '\n'
        writer.write(request_line.encode())
        await writer.drain()
        
        # Test hello tool
        hello_request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "hello",
                "arguments": {"name": "stdio-over-tcp test"}
            },
            "id": 2
        }
        
        request_line = json.dumps(hello_request) + '\n'
        writer.write(request_line.encode())
        await writer.drain()
        
        response_line = await reader.readline()
        response = json.loads(response_line.decode().strip())
        
        if 'result' in response:
            result = response["result"]["structuredContent"]["result"]
            print(f"✅ Hello tool result: {result}")
        else:
            print(f"❌ Unexpected response: {response}")
        
        # Close connection
        writer.close()
        await writer.wait_closed()
        
        print("🎉 stdio-over-tcp transport test successful!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        await cleanup_server(server_process)

async def cleanup_server(process):
    """Cleanup server process and all children."""
    try:
        # Kill entire process group
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        
        # Wait for graceful shutdown
        try:
            await asyncio.wait_for(process.wait(), timeout=3.0)
        except asyncio.TimeoutError:
            # Force kill if needed
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            await process.wait()
            
    except ProcessLookupError:
        # Process already dead
        pass
    
    print("Server cleanup complete")

if __name__ == "__main__":
    try:
        asyncio.run(test_stdio_over_tcp())
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)