# Damien MCP Server Deployment Guide

This guide will help you deploy the Damien MCP Server locally and expose it using ngrok for Claude integration.

## Step 1: Verify Server Configuration

The environment has been checked and updated:
- All paths to Gmail token and credentials files are valid
- DynamoDB table 'DamienMCPSessions' is active
- Log level has been set to DEBUG for better visibility

## Step 2: Start the Damien MCP Server

Run the following command in a terminal:

```bash
cd /Users/ivanrivera/Downloads/AWS/DamienPlatform/damien_mcp_server
/Users/ivanrivera/.local/bin/poetry run uvicorn damien_mcp_server.main:app --host 0.0.0.0 --port 8892 --reload
```

You should see output indicating that the server is running on http://0.0.0.0:8892

## Step 3: Verify Server is Accessible

In another terminal, run:

```bash
# Check health endpoint
curl http://localhost:8892/health

# Check protected endpoint (requires API key)
curl -H "X-API-Key: FiVz_QjpHbfffIktJOip_HKByZhqWTvDlDRv0kFbGKw" http://localhost:8892/mcp/protected-test

# Check Gmail connection
curl -H "X-API-Key: FiVz_QjpHbfffIktJOip_HKByZhqWTvDlDRv0kFbGKw" http://localhost:8892/mcp/gmail-test
```

All endpoints should return successful responses.

## Step 4: Expose with ngrok

### Option 1: Using ngrok CLI (if installed)

If you have ngrok installed and authenticated:

```bash
ngrok http 8892
```

### Option 2: Using our Python tunnel script

1. Create an ngrok account at https://dashboard.ngrok.com if you don't have one
2. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken
3. Run our tunnel script:

```bash
cd /Users/ivanrivera/Downloads/AWS/DamienPlatform/damien_mcp_server
/Users/ivanrivera/.local/bin/poetry run python tools/tunnel.py
```

When prompted, enter your ngrok authtoken.

## Step 5: Configure Claude

Once ngrok is running, you'll see a public URL like: https://a1b2-203-0-113-42.ngrok-free.app

When configuring Claude via the Anthropic API or console:

1. Use the endpoint URL: `https://a1b2-203-0-113-42.ngrok-free.app/mcp/execute_tool`
2. Use the API Key: `FiVz_QjpHbfffIktJOip_HKByZhqWTvDlDRv0kFbGKw`
3. Use the tool schemas from: `/Users/ivanrivera/Downloads/AWS/DamienPlatform/damien_mcp_server/tools/schemas/damien_all_tools.json`

## Step 6: Test with Claude

After configuring Claude, start with simple requests like:
- "List my 5 most recent emails"
- "Show me emails from example@domain.com"

Monitor:
- The ngrok interface (usually at http://localhost:4040)
- The Damien MCP Server logs in the terminal
- Claude's responses and tool use

## Troubleshooting

- If ngrok shows errors about the tunnel, try restarting the tunnel
- If Claude can't connect, verify the API key is being sent correctly
- If Gmail operations fail, check the token permissions and expiration
