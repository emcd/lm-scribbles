#!/usr/bin/env python3
"""
Integration test utility that properly manages server processes.
"""

import asyncio
import json
import contextlib
import sys
import signal
import os

class MCPTestServer:
    """Context manager for MCP server testing with proper cleanup."""
    
    def __init__(self, port: int):
        self.port = port
        self.process = None
        
    async def __aenter__(self):
        """Start the MCP server."""
        print(f"Starting MCP server on port {self.port}...")
        
        # Start server with proper process group for easier cleanup
        self.process = await asyncio.create_subprocess_exec(
            'hatch', 'run', 'sphinxmcps', 'serve', '--port', str(self.port),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            preexec_fn=os.setsid  # Create new process group
        )
        
        # Wait for server to start
        await asyncio.sleep(1)
        
        # Check if server started successfully
        if self.process.returncode is not None:
            stdout, stderr = await self.process.communicate()
            raise RuntimeError(f"Server failed to start: {stderr.decode()}")
            
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Stop the MCP server and cleanup all processes."""
        if self.process:
            try:
                # Kill entire process group to cleanup subprocesses
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                
                # Wait for graceful shutdown
                try:
                    await asyncio.wait_for(self.process.wait(), timeout=3.0)
                except asyncio.TimeoutError:
                    # Force kill if needed
                    os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
                    await self.process.wait()
                    
            except ProcessLookupError:
                # Process already dead
                pass
                
        print(f"MCP server on port {self.port} stopped")
        
    async def send_request(self, request: dict) -> dict:
        """Send MCP request and get response."""
        reader, writer = await asyncio.open_connection('localhost', self.port)
        try:
            # Send request
            request_line = json.dumps(request) + '\n'
            writer.write(request_line.encode())
            await writer.drain()
            
            # Read response
            response_line = await reader.readline()
            return json.loads(response_line.decode().strip())
            
        finally:
            writer.close()
            await writer.wait_closed()


async def test_mcp_protocol():
    """Test complete MCP protocol flow."""
    port = 8010
    
    async with MCPTestServer(port) as server:
        # Initialize
        init_response = await server.send_request({
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"roots": {"listChanged": True}, "sampling": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            },
            "id": 1
        })
        
        print("✅ Initialize:", init_response["result"]["serverInfo"]["name"])
        
        # Send initialized notification (no response expected)
        await server.send_request({
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        })
        
        # List tools
        tools_response = await server.send_request({
            "jsonrpc": "2.0",
            "method": "tools/list",
            "id": 2
        })
        
        tools = [tool["name"] for tool in tools_response["result"]["tools"]]
        print("✅ Tools available:", tools)
        
        # Test hello tool
        hello_response = await server.send_request({
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "hello",
                "arguments": {"name": "Integration Test"}
            },
            "id": 3
        })
        
        result = hello_response["result"]["structuredContent"]["result"]
        print("✅ Hello tool:", result)
        
        print("🎉 All tests passed!")


if __name__ == "__main__":
    try:
        asyncio.run(test_mcp_protocol())
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)