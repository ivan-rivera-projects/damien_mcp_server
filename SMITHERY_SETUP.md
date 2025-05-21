# Setting Up Damien in Smithery.ai

This guide walks you through the process of integrating your Damien MCP Server with Smithery.ai for Claude access.

## Prerequisites

- Active Smithery.ai account
- Running Damien MCP Server (exposed via ngrok)
- Damien tool schemas (from `/tools/schemas/damien_all_tools.json`)

## Step 1: Create a New AI Tool in Smithery

1. Log in to your Smithery.ai account
2. Navigate to the "Create Tool" or similar section
3. Select "API Proxy" or "External API" as the tool type

## Step 2: Configure the Damien MCP Connection

Enter the following details:

- **Tool Name**: Damien Email Manager
- **Description**: Gmail management tool for automating email actions
- **Icon**: (Optional) Upload an email-related icon

### API Configuration:

- **Endpoint URL**: `https://b705-2603-8000-d003-a71d-ad8c-ccb6-c73a-7c/mcp/execute_tool`
- **Method**: POST
- **Headers**:
  - Key: `X-Api-Key`
  - Value: `FiVz_QjpHbfffIktJOip_HKByZhqWTvDlDRv0kFbGKw`
- **Content Type**: application/json

## Step 3: Configure Tool Schemas

In the schema configuration section:

1. **Upload JSON Schema**: Upload the `damien_all_tools.json` file or
2. **Paste Schema**: Copy and paste the contents of the schema file

If Smithery requires individual tool definitions, you can upload or paste each tool schema from the `/tools/schemas/` directory individually.

## Step 4: Set Authorization and Access

Configure who can access this tool:

- **Private**: For your personal use only
- **Shared**: For specific users/teams
- **Public**: For all Smithery users (not recommended for personal email access)

## Step 5: Deploy the Tool

Follow Smithery's process to deploy your tool. This may include:
- Testing the connection
- Setting usage limits
- Confirming deployment

## Step 6: Integrate with Claude

Once deployed, Smithery should provide:

1. A permanent URL for your tool
2. Configuration for Claude to access it
3. A streamlined way to add this tool to your Claude conversations

Depending on Smithery's interface:
- You might get a direct "Add to Claude" option
- You might need to copy configuration details to add in Anthropic Console

## Step 7: Test Integration

Test your integration with simple commands:

1. "List my 5 most recent unread emails"
2. "Show me emails from [specific sender]"
3. "What's the subject of the most recent email?"

## Maintaining the Integration

Remember:
- Keep your Damien MCP Server running
- If using the free ngrok, update the URL in Smithery whenever it changes
- Consider upgrading to a permanent ngrok URL for stability

## Troubleshooting

- **Connection Errors**: Verify ngrok is running and the URL is current
- **Authentication Errors**: Check that the API key is correctly configured
- **Schema Errors**: Validate that your tool schemas match Smithery's requirements
