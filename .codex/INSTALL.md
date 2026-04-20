# Installing Bundles Forge for Codex

Enable skills in Codex via native skill discovery. Clone and symlink.

## Prerequisites

- Git

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/odradekai/bundles-forge.git ~/.codex/bundles-forge
   ```

2. **Create symlinks for skills and agents:**
   ```bash
   mkdir -p ~/.agents/skills ~/.agents/agents
   ln -s ~/.codex/bundles-forge/skills ~/.agents/skills/bundles-forge
   ln -s ~/.codex/bundles-forge/agents ~/.agents/agents/bundles-forge
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\agents"
   cmd /c mklink /J "$env:USERPROFILE\.agents\skills\bundles-forge" "$env:USERPROFILE\.codex\bundles-forge\skills"
   cmd /c mklink /J "$env:USERPROFILE\.agents\agents\bundles-forge" "$env:USERPROFILE\.codex\bundles-forge\agents"
   ```

3. **Restart Codex** to discover skills and agents.

## Updating

```bash
cd ~/.codex/bundles-forge && git pull
```

Skills update instantly through the symlink.

## Uninstalling

```bash
rm ~/.agents/skills/bundles-forge
rm ~/.agents/agents/bundles-forge
rm -rf ~/.codex/bundles-forge
```
