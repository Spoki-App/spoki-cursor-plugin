# Spoki (Cursor / Grok Bot plugin)

WhatsApp messaging for your AI agent, powered by [Spoki](https://www.spoki.com) remote MCP.

Install this plugin in **Cursor** or **Grok Bot** (same marketplace catalog). Your agent talks to Spoki over MCP: contacts, templates, campaigns, automations, lists, tags, tickets, and more. No invented APIs. Tools come from the live Spoki MCP server.

**Repo:** https://github.com/Spoki-App/spoki-cursor-plugin  
**MCP docs:** https://support.spoki.com/en/docs/integrations/get-started-with-spoki-mcp/  
**MCP URL:** `https://mcp.spoki.com/v2/mcp`

---

## What you get

| Piece | Role |
|-------|------|
| `.cursor-plugin/plugin.json` | Marketplace manifest (name `spoki`, category Inbox And Collaboration) |
| `mcp.json` | Remote MCP connection to Spoki |
| `skills/` (optional) | Thin guides: when to use Spoki, how to get an API key |
| `assets/` | Spoki logo for the listing |

This package is **configuration only**. It does not ship Spoki backend code. Runtime is Spoki MCP.

---

## Requirements

- A Spoki account with MCP enabled
- An API key from Spoki → Integrations → Spoki MCP → Request Api Key
- Cursor and/or Grok Bot with Plugins / MCP support

---

## Install

### From the marketplace (recommended)

1. Open Cursor or Grok Bot Plugins.
2. Find **Spoki** under **Inbox And Collaboration**.
3. Install.
4. When prompted, set the plugin variable `SPOKI_API_KEY` to your Spoki MCP API key.
5. Smoke-test: ask the agent to list tags or fetch contacts.

### From this repo (dev / review)

1. Clone: `git clone https://github.com/Spoki-App/spoki-cursor-plugin.git`
2. Install or link the plugin folder in your client (see Cursor plugin docs).
3. Set `SPOKI_API_KEY` (never commit it).
4. Confirm `mcp.json` points at `https://mcp.spoki.com/v2/mcp`.

---

## Auth

Spoki MCP (Cursor / Grok path) uses an HTTP header:

- Header name: `X-Spoki-Api-Key`
- Header value: your Spoki MCP API key

The plugin declares a variable (e.g. `SPOKI_API_KEY`). `mcp.json` references `${SPOKI_API_KEY}` only.

**Never** put API keys in git, screenshots of secrets, or PR descriptions.

Other Spoki MCP auth modes (e.g. Claude OAuth) are documented on support.spoki.com. They are not the default for this Cursor / Grok Bot listing.

---

## Tools (live MCP wins)

After auth, the agent discovers tools via MCP `tools/list`. That live list is the source of truth if docs drift.

Documented surface (checklist from Spoki MCP docs):

- **Contacts:** get/create/update, tags, fields, block, advanced search
- **Automations:** list, get, activate, deactivate, trigger
- **Campaigns:** list, get, create, upcoming events
- **Lists:** CRUD, sync, import jobs, HubSpot / Klaviyo import
- **Templates:** CRUD, submit
- **Tags / tag categories:** CRUD, merge
- **Custom fields:** CRUD, usage
- **Tickets** (if enabled on the account): CRUD, assign, categories
- **Analytics / operators:** contact stats, automation stats, campaign performance, operators

Exact tool names: see Spoki support docs and live `tools/list`.

---

## Example prompts

- "List my Spoki tags."
- "Find or create a contact with phone +39…"
- "Show campaigns and their status."
- "Trigger automation X for contact Y."
- "Draft a WhatsApp template draft (do not submit until I confirm)."

Prefer read / preview before write when the agent can change live account data.

---

## Compatibility

| Client | Support |
|--------|---------|
| Cursor | Primary (marketplace + MCP) |
| Grok Bot | Same marketplace catalog |
| Other MCP clients | You can point any MCP client at `https://mcp.spoki.com/v2/mcp` with `X-Spoki-Api-Key`; this repo is the Cursor Plugin packaging |

---

## Data and privacy

- The plugin stores no Spoki customer data.
- Traffic goes between your agent client and Spoki MCP using **your** API key and account permissions.
- Scope is limited to what Spoki MCP exposes for that account.
- Governed by Spoki Terms and Privacy Policy: https://www.spoki.com

---

## Security checklist

- [ ] API key only in client secrets / plugin variables
- [ ] No keys in README examples (use placeholders)
- [ ] Rotate the key if it leaks
- [ ] Least privilege: use a key from an account role you trust

---

## Troubleshooting

| Symptom | Check |
|---------|--------|
| Tools empty / auth errors | `SPOKI_API_KEY` set? Header name exactly `X-Spoki-Api-Key`? |
| Wrong or missing tools | Re-run live `tools/list`; compare to support docs (updated 2026-09-28+) |
| Tickets tools missing | Feature may be off on the Spoki account |
| Marketplace install fails | Confirm category **Inbox And Collaboration** and plugin name `spoki` |

More: https://support.spoki.com/en/docs/integrations/get-started-with-spoki-mcp/

---

## Development (Spoki team)

Tasks | IT **#6087**. Agent Kit. Plan Review Slave. Marketplace publish: CoS.

Scaffold expected layout:

```text
spoki-cursor-plugin/
├── .cursor-plugin/plugin.json
├── mcp.json
├── skills/          # optional thin skills
├── assets/logo.svg
└── README.md
```

`plugin.json` locks:

- `name`: `spoki`
- `displayName`: `Spoki`
- `repository`: `https://github.com/Spoki-App/spoki-cursor-plugin`
- Category string: **Inbox And Collaboration**

Do not invent MCP endpoints or tool names. Do not use the Unicode em dash character in any copy.

---

## License

MIT (unless Spoki Legal sets otherwise).

---

## Support

- Product docs: https://support.spoki.com  
- Website: https://www.spoki.com  
- Issues: use this GitHub repo Issues for plugin packaging only (MCP server bugs go through Spoki support)

Spoki © Spoki
