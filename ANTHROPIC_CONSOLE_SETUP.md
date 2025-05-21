# Setting Up Damien as a Chat-Accessible Tool in Anthropic Console

This guide explains how to configure Damien as a tool that's directly accessible in Claude chat conversations, similar to Desktop-Commander.

## Overview

Based on the Anthropic documentation for Claude Code MCP setup, custom tools can be registered in the Anthropic Console and made available in the chat interface. This is the same mechanism that powers Desktop-Commander.

## Step 1: Access the Anthropic Console

1. Log in to your Anthropic Console account.
2. Go to the "Tools" or "Integrations" section (the exact name may vary).

## Step 2: Register a New MCP Tool

Look for an option like "Register New Tool" or "Add Custom Tool" and follow these steps:

1. **Basic Information:**
   - Name: "Damien Email Manager"
   - Description: "A tool for managing Gmail using Damien's email management capabilities"

2. **Endpoint Configuration:**
   - Endpoint URL: `https://b705-2603-8000-d003-a71d-ad8c-ccb6-c73a-7c/mcp/execute_tool`
   - Authentication Type: "API Key" or "Header-based"
   - Header Name: "X-Api-Key"
   - Header Value: `FiVz_QjpHbfffIktJOip_HKByZhqWTvDlDRv0kFbGKw`

3. **Tool Definitions:**
   - Upload your `damien_all_tools.json` file, or
   - Paste the content in the provided text area

4. **Permissions:**
   - Set the appropriate permission level (likely "Private" for personal use)
   - Specify which of your Claude instances should have access to this tool

## Step 3: Test in Chat Interface

Once registered, start a new chat in the Claude interface where the tool is enabled.

You should be able to:
1. Use natural language to ask Claude to perform email operations
2. See Claude use Damien tools similar to how it uses Desktop-Commander
3. Potentially see a "Damien" tool option in the interface (depending on how Anthropic Console displays tools)

## Troubleshooting

If you don't see Damien available in your chat interface after configuration:

1. **Check Tool Status:**
   - Verify the tool shows as "Active" in the Anthropic Console
   - Make sure it's associated with the correct Claude instance

2. **Verify Permissions:**
   - Ensure the tool is authorized for your account/conversation
   - Some tools may require additional approval from Anthropic

3. **Browser Issues:**
   - Try refreshing your browser or starting a new conversation
   - Clear cache and cookies if necessary

4. **Contact Anthropic Support:**
   - If all else fails, Anthropic Support can help with tool registration issues

## Important Notes

- The exact UI and workflow in Anthropic Console may differ from what's described here
- Tool registration might require verification or approval from Anthropic
- The process may change as the Anthropic Console evolves

Follow the on-screen instructions in the Anthropic Console, as they are the most up-to-date guidance.
