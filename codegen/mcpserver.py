#use FastMCP to implement a remote MCP server
import json
from typing import Dict, Any    
from fastmcp import FastMCP

# create an instance of the FastMCP server
mcp = FastMCP("Hello World")

@mcp.tool()
def echo(message: str) -> str:
    """Echo the input message"""
    return message

@mcp.tool()
def initialize() -> Dict[str, str]:
    """Initialize the MCP server"""
    return {"status": "MCP server initialized", "version": "1.0"}

def _send_request(self, endpoint: str, data: Dict[str, Any] = None) -> Dict:
    """Send a request to the MCP server"""
    url = f"{self.server_url}/{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data) if data else None)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}


@mcp.tool()
def list_tools() -> Dict[str, Any]:
    """List all available tools"""
    return mcp.list_tools()

@mcp.tool()
def get_tool_info(tool_name: str) -> Dict[str, Any]:
    """Get information about a specific tool"""
    return mcp.get_tool_info(tool_name)

@mcp.tool()
def call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Call a specific tool with given arguments"""
    return mcp.call_tool(name, arguments)

@mcp.tool()
def list_resources() -> Dict[str, Any]:
    """List all available resources"""
    return mcp.list_resources()

@mcp.tool()
def get_resource_info(resource_name: str) -> Dict[str, Any]:
    """Get information about a specific resource"""
    return mcp.get_resource_info(resource_name)

@mcp.tool()
def read_resource(uri: str) -> Dict[str, Any]:
    """Read a specific resource by its URI"""
    return mcp.read_resource(uri)

@mcp
