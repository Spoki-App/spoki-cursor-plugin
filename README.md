# Spoki

WhatsApp Business, from Cursor and Grok Bot.

Install the plugin, drop in your Spoki API key, and your agent can work inside your Spoki account the same way you do in the dashboard. Contacts. Lists. Tags. Templates. Automations. Campaigns. Tickets. Stats. No copy-paste between tools.

## Why bother

You already talk to your agent all day. Spoki is where your customers actually are. This plugin closes that gap.

Ask once. The agent hits Spoki’s live MCP server and does the work.

- “Find everyone tagged VIP who isn’t blocked and put them on a list for Friday’s drop.”
- “Draft a campaign for that list with our birthday template and show me what’s scheduled.”
- “Open a ticket for this contact and assign it to support.”
- “How many contacts do we have, and which campaigns actually performed?”

That’s the product. Not a toy demo. Real account data, real actions.

## What you can do

Everything below is what Spoki MCP exposes today. Your client discovers tools live, so the list on your account may grow as Spoki ships more. Tickets only show up if tickets are enabled on the account.

### Contacts
Search and list contacts. Pull one by ID. Get-or-create by phone. Update profile fields. Block or unblock. Add and remove tags. Read tags on a contact. Set custom field values. Run advanced searches across tags, lists, language, email, and more.

### Automations
List automations. Inspect one. Turn them on or off. Trigger an active automation for a specific contact.

### Campaigns
List scheduled campaigns. Inspect one. Create a new scheduled campaign. Pull upcoming holidays and events when you’re planning.

### Lists
Browse and fetch lists. Create, update, delete. Build a list from filters. Sync contacts by ID or by filter. Remove members (by ID, by filter, or clear the list). Check an import job. Import contacts from HubSpot or Klaviyo into a new Spoki list.

### Templates
List templates (search and approval status). Fetch one with localizations and components. Create, update, delete. Submit a template for WhatsApp provider approval.

### Tags
List, create, update, delete tags. Merge one tag into another (contacts move with it). Manage tag categories.

### Custom fields
List and fetch custom fields. Create, update, delete. See where a field is used across automations and templates.

### Tickets
Browse and search tickets. Fetch one. Create and update. Close. Assign to an operator (or unassign). List ticket categories.

### Analytics and operators
Contact totals plus list and tag counts. Automation totals (including active). Campaign performance breakdown. Operators on the account and their roles.

## Install

1. Install **Spoki** from the Cursor / Grok Bot marketplace (category: Inbox And Collaboration).
2. Open plugin settings and set `SPOKI_API_KEY`.
3. Confirm the `spoki` MCP server shows as connected with a tool list.

### Get the API key

1. Sign in at [app.spoki.com](https://app.spoki.com).
2. Go to **Integrations → Spoki MCP → Request Api Key**.
3. Paste the key into the plugin variable. Treat it like a password. Anyone with it can act as your Spoki account.

Manual MCP (same server the plugin uses):

```json
{
  "mcpServers": {
    "spoki": {
      "url": "https://mcp.spoki.com/v2/mcp",
      "headers": {
        "X-Spoki-Api-Key": "YOUR_API_KEY"
      }
    }
  }
}
```

## Smoke test

After install, ask something small and true for your account:

- “What tags do I have in Spoki?”
- “List my active automations.”
- “Show approved WhatsApp templates.”

If the answers match the dashboard, you’re good.

## Skills in this plugin

Thin helpers so the agent knows when to reach for Spoki and how to get a key. They do not invent APIs. The MCP tool catalogue is the source of truth.

## Notes

- Server: `https://mcp.spoki.com/v2/mcp` (Streamable HTTP).
- Auth header: `X-Spoki-Api-Key` via the `SPOKI_API_KEY` plugin variable. Nothing secret belongs in the repo.
- Same endpoint works for Cursor Cloud Agents once the key is configured.
- Docs: [Get Started with Spoki MCP](https://support.spoki.com/en/docs/integrations/get-started-with-spoki-mcp/)

## Links

- [spoki.com](https://spoki.com)
- [app.spoki.com](https://app.spoki.com)
- Support: support@spoki.com

## License

MIT
