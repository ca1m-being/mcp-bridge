from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Claude-ChatGPT-Bridge")

# In-memory queue to store messages between the two AIs
shared_inbox = []

@mcp.tool()
def send_message(sender: str, message: str) -> str:
    """Send a message to the shared inbox for the other AI to read."""
    shared_inbox.append({"sender": sender, "message": message})
    return f"Message from {sender} successfully stored in the bridge."

@mcp.tool()
def read_inbox() -> list:
    """Retrieve all messages currently stored in the bridge inbox."""
    return shared_inbox

if __name__ == "__main__":
    # Run using the standard SSE transport layout
    mcp.run(transport="sse")
