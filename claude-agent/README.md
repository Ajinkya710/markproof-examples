# Claude agent + Markproof MCP server

A Claude agent (Anthropic Python SDK tool runner) that marks the images it produces with the [Markproof MCP server](https://www.npmjs.com/package/markproof-mcp): invisible watermark + signed C2PA Content Credentials, for EU AI Act Article 50. It then verifies the result.

```bash
pip install -r requirements.txt          # Python 3.10+; Node 18+ for npx
export ANTHROPIC_API_KEY=...
export MARKPROOF_API_KEY=lt_live_...     # https://markproof.co/dashboard
python agent.py path/to/generated.png
```

The MCP server exposes three tools: `mark_file` (writes `<name>.marked.png` next to the original, optional `visible_label`), `verify_file` and `get_asset`. The agent gets them through `async_mcp_tool`, so adding Markproof to an existing tool-runner agent is the `stdio_client` block plus one line in `tools=`.

**Claude Desktop / Claude Code instead?** No code needed. Add the server to your MCP config:

```json
{
  "mcpServers": {
    "markproof": {
      "command": "npx",
      "args": ["-y", "markproof-mcp"],
      "env": { "MARKPROOF_API_KEY": "lt_live_..." }
    }
  }
}
```
