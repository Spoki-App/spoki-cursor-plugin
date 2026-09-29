# Spoki (Cursor / Grok Bot plugin)

<img src="assets/logo.svg" alt="Spoki" width="96" height="96">

WhatsApp messaging for your AI agent, powered by [Spoki](https://www.spoki.com) remote MCP.

Install this plugin in **Cursor** or **Grok Bot** (same marketplace catalog). Your agent talks to Spoki over MCP: contacts, templates, campaigns, automations, lists, tags, tickets, and more. No invented APIs. Tools come from the live Spoki MCP server.

**Repo:** https://github.com/Spoki-App/spoki-cursor-plugin  
**MCP docs:** https://support.spoki.com/en/docs/integrations/get-started-with-spoki-mcp/  
**MCP URL:** `https://mcp.spoki.com/v2/mcp`

---

## What you get

| Piece | Role |
|-------|------|
| `.cursor-plugin/plugin.json` | Marketplace manifest (name `spoki`, category Inbox And Collaboration). Declares the `SPOKI_API_KEY` variable. |
| `mcp.json` | Remote MCP connection to Spoki (Streamable HTTP, `X-Spoki-Api-Key` header) |
| `skills/spoki/SKILL.md` | Thin guide: when to use Spoki, how to get an API key |
| `assets/logo.svg` | Spoki logo for the listing |
| `scripts/smoke_test.py` | Optional key check against the live server (Python 3, standard library only) |

The plugin is **configuration only**. It does not ship Spoki backend code. Runtime is Spoki MCP. The smoke test script is a helper you run yourself. The plugin never runs it.

---

## Requirements

- A Spoki account with MCP enabled
- An API key from Spoki → Integrations → Spoki MCP → Request Api Key (see [Get your API key](#get-your-api-key))
- Cursor and/or Grok Bot with Plugins / MCP support

---

## Install

### From the marketplace (recommended)

1. Open Cursor or Grok Bot Plugins. In Cursor, open **Customize**. In Grok Bot, select **Plugins** in the sidebar (mobile app: tap your avatar, then **Plugins**).
2. Find **Spoki** under **Inbox And Collaboration**.
3. Install.
4. When prompted, set the plugin variable `SPOKI_API_KEY` to your Spoki MCP API key. To change it later in Cursor, open **Plugins** in the Cursor dashboard and select **Configure** on Spoki.
5. Smoke-test: ask the agent to list tags or fetch contacts. See [Smoke test](#smoke-test).

### From this repo (dev / review)

1. Clone into Cursor's local plugins folder. Cursor skips symlinks that point to a folder elsewhere on disk, so clone or copy instead of linking.

   ```bash
   git clone https://github.com/Spoki-App/spoki-cursor-plugin.git ~/.cursor/plugins/local/spoki
   ```

2. Run **Developer: Reload Window**. In **Customize**, check that the Spoki plugin, its `spoki` MCP server, and the `spoki` skill are listed.
3. Set `SPOKI_API_KEY` with **Configure** on the plugin (never commit it). If **Configure** isn't available for a local copy, use the manual setup below.
4. Confirm `mcp.json` points at `https://mcp.spoki.com/v2/mcp`.

On Teams and Enterprise plans, an admin must turn on **Allow Local Plugin Imports**.

### Manual setup without the plugin

Add the server to `~/.cursor/mcp.json` and keep the key in an environment variable named `SPOKI_API_KEY`, which Cursor reads at startup:

```json
{
  "mcpServers": {
    "spoki": {
      "url": "https://mcp.spoki.com/v2/mcp",
      "headers": {
        "X-Spoki-Api-Key": "${env:SPOKI_API_KEY}"
      }
    }
  }
}
```

---

## Auth

Spoki MCP (Cursor / Grok path) uses an HTTP header:

- Header name: `X-Spoki-Api-Key`
- Header value: your Spoki MCP API key

The plugin declares the `SPOKI_API_KEY` variable, and `mcp.json` references `${SPOKI_API_KEY}` only.

### Get your API key

1. Log in to Spoki at [app.spoki.com](https://app.spoki.com) and go to **Integrations** → **Spoki MCP** → **Request Api Key**.
2. Copy the key.
3. Keep it private. Anyone who has the key can use your Spoki account.

**Never** put API keys in git, screenshots of secrets, or PR descriptions.

Other Spoki MCP auth modes (e.g. Claude OAuth) are documented on support.spoki.com. They are not the default for this Cursor / Grok Bot listing.

---

## Smoke test

### 1. Check the key from a terminal

`scripts/smoke_test.py` connects to the server, prints the live `tools/list`, and lists your tags with `get_tags`, which only reads data. `read -rs` keeps the key out of your shell history.

```bash
read -rs SPOKI_API_KEY && export SPOKI_API_KEY
python3 scripts/smoke_test.py
```

A working key prints `Connected: ...`, then the live tool list, then your tags and `Smoke test passed.` A wrong or inactive key prints `invalid_api_key`.

Without a checkout, use Spoki's `curl` check. A valid key returns a response that contains `"serverInfo"`.

```bash
curl -X POST https://mcp.spoki.com/v2/mcp \
  -H "X-Spoki-Api-Key: $SPOKI_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

### 2. List tags from the agent

In Cursor or Grok Bot, ask:

> What tags do I have in Spoki?

The agent should call Spoki's tag tool (`get_tags`) and answer with the tags in your account.

---

## Tools (live MCP wins)

After auth, the agent discovers tools via MCP `tools/list`. That live list is the source of truth if docs drift.

Documented surface (checklist from Spoki MCP docs):

- **Contacts:** get/create/update, tags, fields, block, advanced search
- **Automations:** list, get, activate, deactivate, trigger
- **Campaigns:** list, get, create, upcoming events
- **Lists:** CRUD, sync, import jobs, HubSpot / Klaviyo import
- **Templates:** CRUD, submit
- **Tags / tag categories:** tags CRUD and merge; tag categories list and create
- **Custom fields:** CRUD, usage
- **Tickets** (if enabled on the account): list, get, create, update, close, assign, categories
- **Analytics / operators:** contact stats, automation stats, campaign performance, operators

Exact tool names: see [Spoki support docs](https://support.spoki.com/en/docs/integrations/get-started-with-spoki-mcp/#supported-tools--actions) and live `tools/list`.

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
| Grok Bot | Same marketplace catalog. `mcp.json` sets `"placement": "server"`, which Grok Bot requires before it connects to a plugin's MCP server. |
| Other MCP clients | You can point any MCP client at `https://mcp.spoki.com/v2/mcp` with `X-Spoki-Api-Key`; this repo is the Cursor Plugin packaging |

---

## Data and privacy

- The plugin stores no Spoki customer data.
- Traffic goes between your agent client and Spoki MCP using **your** API key and account permissions. Grok Bot sends it through Cursor's hosted MCP connection.
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
| `invalid_api_key` (`invalid or inactive X-Spoki-Api-Key`) | The key is wrong or inactive, or the variable was not filled in. Re-enter `SPOKI_API_KEY` or request a new key. |
| `No bearer access token was provided` | No key reached Spoki. Set `SPOKI_API_KEY` on the plugin. |
| Wrong or missing tools | Re-run live `tools/list` (`python3 scripts/smoke_test.py`); compare to support docs (updated 2026-09-28+) |
| Tickets tools missing | Feature may be off on the Spoki account |
| Marketplace install fails | Confirm category **Inbox And Collaboration** and plugin name `spoki` |

In Cursor, connection errors appear in the **Output** panel under **MCP Logs**.

More: https://support.spoki.com/en/docs/integrations/get-started-with-spoki-mcp/

---

## Development (Spoki team)

Tasks | IT **#6087**. Agent Kit. Plan Review Slave. Marketplace publish: CoS.

Layout:

```text
spoki-cursor-plugin/
├── .cursor-plugin/plugin.json
├── mcp.json
├── skills/spoki/SKILL.md   # thin skill
├── assets/logo.svg
├── scripts/smoke_test.py   # optional key check, not run by the plugin
├── LICENSE
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

[MIT](LICENSE) (unless Spoki Legal sets otherwise).

---

## Support

- Product docs: https://support.spoki.com  
- Email: support@spoki.com  
- Website: https://www.spoki.com  
- Issues: use this GitHub repo Issues for plugin packaging only (MCP server bugs go through Spoki support)

Spoki © Spoki
