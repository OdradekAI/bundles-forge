# Installing <Project Name> for OpenClaw

OpenClaw recognises Claude bundle format automatically. Install from ClawHub or locally.

## From ClawHub

```bash
openclaw bundles install clawhub:<project-name>
```

## From a local directory

```bash
openclaw plugins install ./<project-name>
```

## Verify

```bash
openclaw plugins inspect <project-name>
```

The output should show `Format: bundle` with skills listed under capabilities.

## Updating

```bash
openclaw plugins update <project-name>
```

## Uninstalling

```bash
openclaw plugins uninstall <project-name>
```
