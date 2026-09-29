#!/usr/bin/env python3
"""Smoke-test a Spoki API key against the Spoki MCP server.

Connects over Streamable HTTP, prints the live tool catalog from tools/list,
then lists tags with get_tags (read-only) if the server exposes that tool.

Usage:
    SPOKI_API_KEY=your-key python3 scripts/smoke_test.py

Standard library only. The key is read from the environment and never printed.
"""

import json
import os
import sys
import urllib.error
import urllib.request

MCP_URL = "https://mcp.spoki.com/v2/mcp"
PROTOCOL_VERSION = "2025-06-18"
TIMEOUT_SECONDS = 30
PREVIEW_CHARS = 1500


class McpError(Exception):
    pass


class McpSession:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
        self.session_id = None
        self.protocol_version = None
        self.next_id = 1

    def _headers(self):
        headers = {
            "X-Spoki-Api-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": "spoki-cursor-plugin-smoke-test/1.0",
        }
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        if self.protocol_version:
            headers["MCP-Protocol-Version"] = self.protocol_version
        return headers

    def _open(self, payload, method="POST"):
        data = json.dumps(payload).encode() if payload is not None else None
        request = urllib.request.Request(self.url, data=data, headers=self._headers(), method=method)
        try:
            response = urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS)
        except urllib.error.HTTPError as error:
            raise McpError(f"HTTP {error.code}: {describe_http_error(error)}") from None
        session_id = response.headers.get("Mcp-Session-Id")
        if session_id:
            self.session_id = session_id
        return response

    def request(self, method, params=None):
        message_id = self.next_id
        self.next_id += 1
        payload = {"jsonrpc": "2.0", "id": message_id, "method": method}
        if params is not None:
            payload["params"] = params
        with self._open(payload) as response:
            for message in read_messages(response):
                if message.get("id") != message_id:
                    continue
                if "error" in message:
                    error = message["error"]
                    raise McpError(f"{method} failed: {error.get('message', error)}")
                return message.get("result", {})
        raise McpError(f"{method}: the server closed the response without a result")

    def notify(self, method):
        with self._open({"jsonrpc": "2.0", "method": method}):
            pass

    def close(self):
        if not self.session_id:
            return
        try:
            with self._open(None, method="DELETE"):
                pass
        except (McpError, OSError):
            pass


def describe_http_error(error):
    body = error.read().decode("utf-8", "replace").strip()
    try:
        parsed = json.loads(body)
    except ValueError:
        return body or error.reason
    if isinstance(parsed, dict) and "error" in parsed:
        description = parsed.get("error_description")
        return f"{parsed['error']} ({description})" if description else str(parsed["error"])
    return body


def read_messages(response):
    """Yield JSON-RPC messages from a JSON or text/event-stream response.

    SSE is read incrementally so a stream the server keeps open does not block
    once the matching response has arrived.
    """
    content_type = response.headers.get("Content-Type", "")
    if "text/event-stream" not in content_type:
        body = response.read().decode("utf-8")
        if body.strip():
            yield from as_list(json.loads(body))
        return
    data_lines = []
    for raw_line in response:
        line = raw_line.decode("utf-8").rstrip("\r\n")
        if line.startswith("data:"):
            value = line[len("data:"):]
            data_lines.append(value[1:] if value.startswith(" ") else value)
        elif line == "" and data_lines:
            yield from as_list(json.loads("\n".join(data_lines)))
            data_lines = []
    if data_lines:
        yield from as_list(json.loads("\n".join(data_lines)))


def as_list(message):
    return message if isinstance(message, list) else [message]


def list_tools(session):
    tools, cursor = [], None
    while True:
        result = session.request("tools/list", {"cursor": cursor} if cursor else {})
        tools.extend(result.get("tools", []))
        cursor = result.get("nextCursor")
        if not cursor:
            return tools


def text_preview(result):
    parts = [item.get("text", "") for item in result.get("content", []) if item.get("type") == "text"]
    text = "\n".join(parts).strip()
    if not text and "structuredContent" in result:
        text = json.dumps(result["structuredContent"], indent=2)
    return text if len(text) <= PREVIEW_CHARS else text[:PREVIEW_CHARS] + "\n..."


def run(url, api_key):
    session = McpSession(url, api_key)
    try:
        init = session.request(
            "initialize",
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "spoki-cursor-plugin-smoke-test", "version": "1.0"},
            },
        )
        session.protocol_version = init.get("protocolVersion", PROTOCOL_VERSION)
        info = init.get("serverInfo", {})
        print(f"Connected: {info.get('name', '?')} {info.get('version', '')} (protocol {session.protocol_version})")
        session.notify("notifications/initialized")

        tools = list_tools(session)
        print(f"\nLive tools from tools/list ({len(tools)}):")
        for tool in sorted(tools, key=lambda item: item.get("name", "")):
            summary = (tool.get("description") or "").strip().splitlines()
            print(f"  - {tool.get('name')}: {summary[0] if summary else ''}")

        if not any(tool.get("name") == "get_tags" for tool in tools):
            print("\nget_tags is not in this account's catalog, so the tag check was skipped.")
            return 0
        result = session.request("tools/call", {"name": "get_tags", "arguments": {}})
        print("\nget_tags:")
        print(text_preview(result) or "(empty result)")
        if result.get("isError"):
            print("\nSmoke test failed: get_tags returned an error.", file=sys.stderr)
            return 1
        print("\nSmoke test passed.")
        return 0
    finally:
        session.close()


def main():
    api_key = os.environ.get("SPOKI_API_KEY", "").strip()
    if not api_key:
        print("Set SPOKI_API_KEY first: SPOKI_API_KEY=your-key python3 scripts/smoke_test.py", file=sys.stderr)
        return 2
    try:
        return run(MCP_URL, api_key)
    except McpError as error:
        print(f"Smoke test failed: {error}", file=sys.stderr)
        return 1
    except (OSError, ValueError) as error:
        print(f"Smoke test failed: could not talk to {MCP_URL}: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
