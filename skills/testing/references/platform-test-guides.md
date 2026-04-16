# Platform-Specific Test Guides

Detailed setup and verification instructions for testing a bundle-plugin on each supported platform.

## Claude Code

### Setup

```bash
# Create dev-marketplace adjacent to your project
mkdir -p ../dev-marketplace/.claude-plugin

# Generate marketplace.json (replace placeholders)
cat > ../dev-marketplace/.claude-plugin/marketplace.json << 'EOF'
{
  "name": "<project-name>-dev",
  "owner": { "name": "dev" },
  "plugins": [
    {
      "name": "<project-name>",
      "source": "../<project-directory>"
    }
  ]
}
EOF

# Add the dev marketplace
# In a Claude Code session:
/plugin marketplace add ../dev-marketplace
/plugin install <project-name>@<project-name>-dev
```

### Verification Checklist

- [ ] `/plugin` lists the installed plugin
- [ ] Skills appear in Skill tool listing
- [ ] Commands appear in `/` menu
- [ ] Agents are discoverable
- [ ] SessionStart hook fires on new session
- [ ] PreToolUse/PostToolUse hooks fire (if configured)
- [ ] `claude plugin validate` passes (if available)

### Cleanup

```bash
/plugin marketplace remove <project-name>-dev
rm -rf ../dev-marketplace
```

## Cursor

### Setup

1. Open Cursor IDE
2. Install from local path: the plugin root directory
3. Reload window (Ctrl+Shift+P → "Reload Window")

### Verification Checklist

- [ ] Skills directory is detected
- [ ] Skills appear in agent's available skills
- [ ] Session hook fires on new chat
- [ ] PreToolUse/PostToolUse hooks fire on edits (if configured)
- [ ] Commands are accessible

### Known Issues

- SessionStart context is lost after `/clear` — the hook re-fires on next session start
- No `${CLAUDE_PLUGIN_ROOT}` equivalent; hooks use relative paths from plugin root

## Codex (CLI)

### Setup

```bash
# Symlink skills into Codex agents directory
ln -sf "$(pwd)/skills" ~/.agents/skills/<project-name>

# Copy AGENTS.md if present
cp AGENTS.md ~/.agents/AGENTS.md  # or merge with existing
```

### Verification Checklist

- [ ] Skills appear in agent skill discovery
- [ ] AGENTS.md references are correct
- [ ] No hook infrastructure needed (Codex reads skills directly)

### Known Issues

- No hook bootstrap mechanism — relies on AGENTS.md and skill directory convention
- Installation is manual (symlink or copy)

## OpenCode

### Setup

```bash
# The .opencode/plugins/<project-name>.js file handles registration
# Verify it exists and exports correctly
node -e "import('./.opencode/plugins/<project-name>.js').then(m => console.log('OK:', Object.keys(m)))"
```

### Verification Checklist

- [ ] Plugin JS file uses ESM (`export default`)
- [ ] Skills path is correctly registered
- [ ] Bootstrap message transform works (prepend to first user message)
- [ ] No double-injection guard issues

### Known Issues

- Plugin JS must be ESM (not CommonJS)
- Tool mapping may differ from Claude Code — check `using-*/references/opencode-tools.md`

## Gemini CLI

### Setup

```bash
# Verify gemini-extension.json
cat gemini-extension.json
# Must have: name, version, description, contextFileName

# Install: point Gemini CLI to the extension
# gemini --extension ./
```

### Verification Checklist

- [ ] `gemini-extension.json` is valid JSON
- [ ] `contextFileName` field points to existing file (e.g. `GEMINI.md`)
- [ ] GEMINI.md contains skill routing context
- [ ] Extension loads without errors

### Known Issues

- Extension installed via git URL — local testing uses directory path
- Tool names differ from Claude Code — verify tool mapping

## OpenClaw

### Setup

OpenClaw uses Claude's plugin infrastructure plus hook-packs.

### Verification Checklist

- [ ] `.claude-plugin/plugin.json` is valid (shared with Claude Code)
- [ ] Hook-pack exists: `hooks/openclaw-bootstrap/HOOK.md` + `handler.js`
- [ ] HOOK.md has valid frontmatter with `events` declaration
- [ ] handler.js uses ESM `export default`
- [ ] Events filter early in handler

### Known Issues

- Hook-pack wiring may not auto-activate for Claude bundles
- Test by manually loading the handler in a Node.js REPL
