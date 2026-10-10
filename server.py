import os
from mcp.server.fastmcp import FastMCP
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# Initialize FastMCP server
mcp = FastMCP("Claude-ChatGPT-Bridge")

# In-memory queue to store messages between the two AIs
shared_inbox = []

# Security Middleware to check the API Key header
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Allow preflight options requests without auth
        if request.method == "OPTIONS":
            return await call_next(request)
            
        auth_header = request.headers.get("Authorization")
        expected_token = f"Bearer {os.environ.get('MCP_API_KEY', 'MeetSecretBridgeToken2026')}"
        
        if not auth_header or auth_header != expected_token:
            return Response("Unauthorized", status_code=401)
            
        return await call_next(request)

# Add the security layer to the underlying Starlette application
mcp.handle_sse().app.add_middleware(AuthMiddleware)

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
    # Run using the SSE transport layout required for remote cloud servers
    mcp.run(transport="sse")
