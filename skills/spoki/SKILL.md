---
name: spoki
description: Use when the user wants to work with their Spoki WhatsApp Business account - contacts, lists, tags, custom fields, message templates, campaigns, automations, support tickets, operators, or account stats - or mentions Spoki. Also use when the Spoki MCP server needs an API key, fails to connect, or returns invalid_api_key.
---

# Spoki

Spoki is a WhatsApp Business platform. This plugin connects the agent to the user's Spoki account through Spoki's remote MCP server, `spoki`, at `https://mcp.spoki.com/v2/mcp`. Every call acts on the real account with the permissions of the API key.

## When to use Spoki

- Finding, creating, updating, tagging, or blocking WhatsApp contacts.
- Building and maintaining contact lists, tags, tag categories, and custom fields.
- Drafting WhatsApp message templates and submitting them for approval.
- Reviewing or scheduling campaigns, and checking campaign performance.
- Listing, switching on or off, or triggering automations for a contact.
- Handling support tickets, when the tickets feature is enabled on the account.
- Answering questions about contact, automation, and campaign stats or the team's operators.

## Tools come from the server

- Use only the tools that the `spoki` server returns from `tools/list`. The catalog depends on the account. For example, ticket tools appear only when tickets are enabled.
- Do not assume a tool exists because Spoki's docs or this skill mention it. If nothing in the list covers the request, tell the user. Do not guess tool names, arguments, or IDs, and do not call Spoki's REST API directly.
- Spoki's published catalog is a reference only: https://support.spoki.com/en/docs/integrations/get-started-with-spoki-mcp/#supported-tools--actions

## Working rules

- Look up IDs with the matching read tool (contact, list, tag, template, automation, campaign, ticket) before acting on them.
- Reads are safe to run. Confirm with the user before any action that reaches people or is hard to undo: triggering an automation, creating a campaign, submitting a template for approval, blocking a contact, merging tags, clearing a list or removing its members, or deleting anything. State exactly what will happen and to whom.
- Never print, log, or repeat the API key.

## API key and connection

1. The user gets a key in Spoki (app.spoki.com): **Integrations → Spoki MCP → Request Api Key**. Anyone with the key can use the account, so it must stay private.
2. The key goes in the plugin's `SPOKI_API_KEY` variable, which is set when the plugin is installed or later under **Plugins → Configure** in the Cursor dashboard. The plugin sends it as the `X-Spoki-Api-Key` header. Never ask the user to paste the key into chat.
3. Errors from the server:
   - `invalid_api_key` (`invalid or inactive X-Spoki-Api-Key`): the key is wrong, revoked, or was not substituted. Ask the user to check the variable or request a new key.
   - `No bearer access token was provided`: no key reached the server. The `SPOKI_API_KEY` variable is empty.
4. More help: https://support.spoki.com/en/docs/integrations/get-started-with-spoki-mcp/ or support@spoki.com.
