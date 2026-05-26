from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet() -> str:
    return f"Hello world!"

if __name__ == "__main__":
    mcp.run()
