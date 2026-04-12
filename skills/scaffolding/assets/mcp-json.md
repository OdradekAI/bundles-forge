# .mcp.json Template

Template for generating `.mcp.json` at the project root. Replace all `<placeholders>` before writing.

## stdio Transport (Bundled Server)

Use when the MCP server ships with the plugin as a local process.

```json
{
  "mcpServers": {
    "<server-name>": {
      "command": "${CLAUDE_PLUGIN_ROOT}/<path-to-server>",
      "args": [],
      "env": {}
    }
  }
}
```

## http Transport (Remote Service)

Use when connecting to an external service endpoint.

```json
{
  "mcpServers": {
    "<server-name>": {
      "type": "http",
      "url": "https://<service-endpoint>/mcp"
    }
  }
}
```

## http Transport with Authentication

Use when the remote service requires a bearer token or API key.

```json
{
  "mcpServers": {
    "<server-name>": {
      "type": "http",
      "url": "https://<service-endpoint>/mcp",
      "headers": {
        "Authorization": "Bearer ${<API_KEY_VAR>}"
      }
    }
  }
}
```

## npm-based stdio (npx Pattern)

Use when the MCP server is distributed as an npm package.

```json
{
  "mcpServers": {
    "<server-name>": {
      "command": "npx",
      "args": ["-y", "<npm-package-name>"],
      "env": {}
    }
  }
}
```

## Placeholder Reference

| Placeholder | Source |
|-------------|--------|
| `<server-name>` | Descriptive kebab-case identifier for the MCP server |
| `<path-to-server>` | Relative path from plugin root to the server executable |
| `<service-endpoint>` | Remote service hostname and path |
| `<API_KEY_VAR>` | Environment variable name holding the API key (never hardcode the value) |
| `<npm-package-name>` | Published npm package name (e.g., `@scope/my-mcp-server`) |
