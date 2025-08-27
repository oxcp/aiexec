# basic import 
from mcp.server.fastmcp import FastMCP
from verifier import Verifier
#from anthropic import Anthropic

# instantiate an MCP server client
mcp = FastMCP("DevHelper")

# DEFINE TOOLS
@mcp.tool()
def code_with_GPT() -> str:
    """verify GPT model for coding"""
    status = Verifier.verify_with_prompt_file(prompt_file="./prompts.txt")
    return status

@mcp.tool()
def code_with_Claude(prompt_file: str) -> str:
    """verify Claude model for coding"""
    return ""

# execute and return the stdio output
if __name__ == "__main__":
    mcp.run(transport="stdio")
