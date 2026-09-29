# Spoki plugin for Cursor and Grok Bot

<img src="assets/logo.svg" alt="Spoki" width="96" height="96">

The Spoki plugin connects Cursor and Grok Bot agents to your [Spoki](https://spoki.com) WhatsApp Business account through Spoki's remote MCP server:

```text
https://mcp.spoki.com/v2/mcp
```

It uses Streamable HTTP and authenticates with your Spoki API key, which it sends in the `X-Spoki-Api-Key` header. The server is remote, so the plugin installs nothing locally. It consists of an MCP server entry, one skill, and a logo.

## What the agent can do

The agent uses the tools that the Spoki server returns at connect time (`tools/list`). That live list is the source of truth, and it depends on your account. Ticket tools, for example, appear only when the tickets feature is enabled. Spoki's published catalog covers:

- **Contacts:** search, get or create by phone, update, block, tag, and set custom field values.
- **Lists:** create and maintain lists, add or remove contacts by ID or by filter, and import from HubSpot or Klaviyo.
- **Tags and custom fields:** create, update, and delete tags and custom fields, merge tags, add tag categories, and see where a custom field is used.
- **Templates:** create, update, and delete WhatsApp message templates, and submit them for approval.
- **Campaigns:** list, schedule, and review campaign performance.
- **Automations:** list, switch on or off, and trigger an automation for a contact.
- **Tickets:** browse, create, assign, and close tickets, if tickets are enabled.
- **Stats and team:** contact, automation, and campaign stats, and the operators on your account.

See [Supported Tools & Actions](https://support.spoki.com/en/docs/integrations/get-started-with-spoki-mcp/#supported-tools--actions) for the current list.

## Get your Spoki API key

1. Log in to Spoki at [app.spoki.com](https://app.spoki.com) and go to **Integrations** → **Spoki MCP** → **Request Api Key**.
2. Copy the key.
3. Keep the key private. Anyone who has it can use your Spoki account. Don't commit it to a repository or paste it into chat.

## Install

### Cursor

1. Open **Customize**, search the marketplace for **Spoki**, and select **Install**.
2. When Cursor asks for `SPOKI_API_KEY`, paste your API key. To change it later, open **Plugins** in the Cursor dashboard and select **Configure** on Spoki.
3. In **Customize**, check that the `spoki` MCP server is connected and lists its tools.

### Grok Bot

1. Select **Plugins** in the sidebar. In the mobile app, tap your avatar in the top left, then select **Plugins**.
2. Search for **Spoki** and add it.
3. Enter your API key when Grok Bot asks for `SPOKI_API_KEY`.
4. Check that Spoki appears under **Installed**.

### Test the plugin before it is listed

Cursor loads unlisted plugins from `~/.cursor/plugins/local`. Clone the repository into that folder. Cursor skips symlinks that point to a folder elsewhere on disk.

```bash
git clone https://github.com/Spoki-App/spoki-cursor-plugin ~/.cursor/plugins/local/spoki
```

Run **Developer: Reload Window**. Then open **Customize** and check that the Spoki plugin, its `spoki` MCP server, and the `spoki` skill are listed. Set `SPOKI_API_KEY` with **Configure** on the plugin. If **Configure** isn't available for a local copy, use the manual setup below instead. On Teams and Enterprise plans, an admin must turn on **Allow Local Plugin Imports**.

### Manual setup without the plugin

You can also add the server to `~/.cursor/mcp.json` yourself. Store the key in an environment variable named `SPOKI_API_KEY`, which Cursor reads at startup:

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

## Smoke test

### 1. Check the key from a terminal

The script needs Python 3 and nothing else. It connects to the server, prints the live `tools/list`, and lists your tags with `get_tags`, which only reads data. `read -rs` keeps the key out of your shell history.

```bash
read -rs SPOKI_API_KEY && export SPOKI_API_KEY
python3 scripts/smoke_test.py
```

A working key prints `Connected: ...`, then the live tool list, then your tags and `Smoke test passed.` A wrong or inactive key prints `invalid_api_key`.

Without a checkout, you can use Spoki's `curl` check. A valid key returns a response that contains `"serverInfo"`.

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

## Troubleshooting

| What you see | What it means | What to do |
| --- | --- | --- |
| `invalid_api_key` or `invalid or inactive X-Spoki-Api-Key` | The key is wrong or inactive, or the variable was not filled in. | Re-enter `SPOKI_API_KEY`, or request a new key in Spoki. |
| `No bearer access token was provided` | The request reached Spoki without a key. | Set `SPOKI_API_KEY` on the plugin. |
| Some tools are missing, such as tickets | The feature is not enabled on your Spoki account. | Enable the feature in Spoki, then reconnect. |

In Cursor, you can find connection errors in the **Output** panel under **MCP Logs**.

## Repository layout

```text
.cursor-plugin/plugin.json   Plugin manifest. Declares the SPOKI_API_KEY variable.
mcp.json                     The remote spoki MCP server.
skills/spoki/SKILL.md        When to use Spoki, API key setup, and working rules for the agent.
assets/logo.svg              Spoki logo.
scripts/smoke_test.py        Checks a key against the live server.
```

`mcp.json` sets `"placement": "server"`. Grok Bot connects only to MCP servers that declare this placement, and routes their calls through Cursor's hosted MCP connection.

This repository contains no secrets. `mcp.json` holds only the `${SPOKI_API_KEY}` placeholder, and you supply the value when you install the plugin.

## Support

- Spoki MCP docs: [Get Started with Spoki MCP](https://support.spoki.com/en/docs/integrations/get-started-with-spoki-mcp/)
- Email: [support@spoki.com](mailto:support@spoki.com)

## License

[MIT](LICENSE)
