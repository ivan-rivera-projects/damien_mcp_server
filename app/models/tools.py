"""Pydantic models for specific MCP tool parameters and outputs.

This module defines the Pydantic models that represent the input parameters
and output structures for each Damien MCP tool. These models are used for:

1. Validating tool parameters from MCP clients
2. Providing JSON schemas for the list_tools endpoint
3. Documenting the expected structure of each tool's inputs and outputs
4. Enabling auto-completion and type checking during development

Each tool typically has a corresponding *Params model for inputs and 
an *Output model for its results. The models leverage Pydantic's validation,
field descriptions, and examples to provide comprehensive documentation.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

from .mcp_protocol import MCPToolCallInput # Base class for tool inputs

# --- damien_list_emails Tool Models ---

class ListEmailsParams(MCPToolCallInput):
    """Parameters for the damien_list_emails tool.
    
    This model defines the parameters for listing emails from Gmail with
    optional filtering, pagination, and limiting the number of results.
    
    Attributes:
        query: Optional Gmail query string to filter emails (e.g., "is:unread")
               See Gmail search operators: https://support.google.com/mail/answer/7190
        max_results: Maximum number of emails to return in a single request
                     (default: 10, must be > 0 and <= 100)
        page_token: Optional token for retrieving the next page of results
                   (obtained from a previous list_emails call)
    
    Example:
        {
            "query": "is:unread from:newsletter@example.com",
            "max_results": 20
        }
    """
    query: Optional[str] = Field(default=None, description="Gmail query string to filter emails (e.g., 'is:unread').")
    max_results: Optional[int] = Field(default=10, description="Maximum number of emails to return.", gt=0, le=100)
    page_token: Optional[str] = Field(default=None, description="Token for retrieving the next page of results.")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "query": "is:unread from:newsletter@example.com",
                "max_results": 20
            }
        }
    )

class EmailSummary(BaseModel):
    """Represents a summary of an email message."""
    id: str = Field(description="The unique ID of the email message.")
    thread_id: Optional[str] = Field(default=None, description="The ID of the email thread.")
    # Future fields: snippet, subject, from, date etc.

class ListEmailsOutput(BaseModel):
    """Output structure for the damien_list_emails tool."""
    email_summaries: List[EmailSummary] = Field(description="List of email summaries.")
    next_page_token: Optional[str] = Field(default=None, description="Token for the next page of results, if any.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email_summaries": [
                    {"id": "123abc456", "thread_id": "thread789"},
                    {"id": "789def012", "thread_id": "thread789"}
                ],
                "next_page_token": "pageTokenForNextSetOfResults"
            }
        }
    )

# --- Add other tool-specific param and output models below ---

# Models moved from old mcp.py

# --- damien_get_email_details Tool Models ---

class GetEmailDetailsParams(MCPToolCallInput):
    """Input model for the damien_get_email_details tool."""
    message_id: str = Field(..., description="The ID of the email message to retrieve.")
    format: Optional[str] = Field(
        default="full",
        description="Format of the email details to retrieve ('full', 'metadata', 'raw')."
    )
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "message_id": "123abc456xyz",
                "format": "full"
            }
        }
    )

class EmailHeader(BaseModel):
    name: str
    value: str

class EmailPartBody(BaseModel):
    attachment_id: Optional[str] = Field(default=None, alias="attachmentId")
    size: int
    data: Optional[str] = None # Base64url encoded string

class EmailPart(BaseModel):
    part_id: Optional[str] = Field(default=None, alias="partId")
    mime_type: Optional[str] = Field(default=None, alias="mimeType")
    filename: Optional[str] = None
    headers: Optional[List[EmailHeader]] = None
    body: Optional[EmailPartBody] = None
    parts: Optional[List['EmailPart']] = None # For multipart messages

EmailPart.model_rebuild() # Ensure forward reference is resolved

class EmailPayload(BaseModel):
    part_id: Optional[str] = Field(default=None, alias="partId")
    mime_type: Optional[str] = Field(default=None, alias="mimeType")
    filename: Optional[str] = None
    headers: Optional[List[EmailHeader]] = None
    body: Optional[EmailPartBody] = None
    parts: Optional[List[EmailPart]] = None

class GetEmailDetailsOutput(BaseModel):
    """Output model for the damien_get_email_details tool."""
    id: str
    thread_id: Optional[str] = Field(default=None, alias="threadId")
    label_ids: Optional[List[str]] = Field(default=None, alias="labelIds")
    snippet: Optional[str] = None
    history_id: Optional[str] = Field(default=None, alias="historyId")
    internal_date: Optional[str] = Field(default=None, alias="internalDate") # Timestamp ms
    payload: Optional[EmailPayload] = None # Present in 'full' format
    size_estimate: Optional[int] = Field(default=None, alias="sizeEstimate")
    raw: Optional[str] = None # Present in 'raw' format
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra = {
            "example": {
                "id": "123abc456xyz",
                "threadId": "thread789",
                "labelIds": ["INBOX", "UNREAD"],
                "snippet": "This is a test email snippet...",
            }
        }
    )

# --- damien_trash_emails Tool Models ---

class TrashEmailsParams(MCPToolCallInput):
    message_ids: List[str] = Field(..., description="A list of message IDs to be moved to trash.")
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {"message_ids": ["123abc456xyz", "789def012uvw"]}
        }
    )

class TrashEmailsOutput(BaseModel):
    trashed_count: int
    status_message: str

# --- damien_label_emails Tool Models ---

class LabelEmailsParams(MCPToolCallInput):
    message_ids: List[str] = Field(..., description="A list of message IDs to label.")
    add_label_names: Optional[List[str]] = Field(None, description="List of label names to add.")
    remove_label_names: Optional[List[str]] = Field(None, description="List of label names to remove.")
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "message_ids": ["123abc456xyz", "789def012uvw"],
                "add_label_names": ["MyCustomLabel"],
                "remove_label_names": ["UNREAD"]
            }
        }
    )

class LabelEmailsOutput(BaseModel):
    modified_count: int
    status_message: str

# --- damien_mark_emails Tool Models ---
# Need to import Literal for this
from typing import Literal, Dict, Any # Added Dict, Any for type aliases

class MarkEmailsParams(MCPToolCallInput):
    message_ids: List[str] = Field(..., description="A list of message IDs to mark as read or unread.")
    mark_as: Literal["read", "unread"] = Field(..., description="Specify whether to mark messages as 'read' or 'unread'.")
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "message_ids": ["123abc456xyz", "789def012uvw"],
                "mark_as": "read"
            }
        }
    )

class MarkEmailsOutput(BaseModel):
    modified_count: int
    status_message: str

# --- damien_apply_rules Tool Models ---

class ApplyRulesParams(MCPToolCallInput):
    gmail_query_filter: Optional[str] = Field(None, description="Base Gmail query string.")
    rule_ids_to_apply: Optional[List[str]] = Field(None, description="Optional list of specific rule IDs.")
    dry_run: bool = Field(False, description="If True, simulates without making changes.")
    scan_limit: Optional[int] = Field(None, description="Optional limit on messages to scan.")
    date_after: Optional[str] = Field(None, description="Apply to emails after this date (YYYY/MM/DD).")
    date_before: Optional[str] = Field(None, description="Apply to emails before this date (YYYY/MM/DD).")
    all_mail: Optional[bool] = Field(False, description="If True, ignores other filters.")
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "gmail_query_filter": "is:unread from:example.com",
                "rule_ids_to_apply": ["rule_123", "rule_456"],
                "dry_run": True,
                "scan_limit": 100,
                "date_after": "2023/01/01",
                "date_before": "2023/12/31",
                "all_mail": False
            }
        }
    )

ApplyRulesOutputData = Dict[str, Any] # Type alias for apply_rules output

# --- damien_list_rules Tool Models ---

ListRulesOutputData = List[Dict[str, Any]] # Type alias for list_rules output

# --- damien_add_rule Tool Models ---

class AddRuleParams(MCPToolCallInput):
    rule_definition: Dict[str, Any] = Field(..., description="Rule definition dictionary. Should conform to damien_cli.features.rule_management.models.RuleModel structure.")
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "rule_definition": {
                    "name": "New MCP Rule", "description": "Test rule.", "is_enabled": True,
                    "conditions": [{"field": "subject", "operator": "contains", "value": "MCP Test"}],
                    "condition_conjunction": "AND",
                    "actions": [{"type": "add_label", "label_name": "MCP_TEST_LABEL"}]
                }
            }
        }
    )

AddRuleOutputData = Dict[str, Any] # Type alias for add_rule output

# --- damien_delete_rule Tool Models ---

class DeleteRuleParams(MCPToolCallInput):
    rule_identifier: str = Field(..., description="The ID or name of the rule to delete.")
    model_config = ConfigDict(
        json_schema_extra = {"example": {"rule_identifier": "unique_rule_id_or_name"}}
    )

class DeleteRuleOutputData(BaseModel):
    status_message: str
    deleted_rule_identifier: str

# --- damien_delete_emails_permanently Tool Models ---

class DeleteEmailsPermanentlyParams(MCPToolCallInput):
    message_ids: List[str] = Field(..., description="List of message IDs for permanent deletion.")
    model_config = ConfigDict(
        json_schema_extra = {"example": {"message_ids": ["perm_del_id_1", "perm_del_id_2"]}}
    )

class DeleteEmailsPermanentlyOutputData(BaseModel):
    deleted_count: int
    status_message: str