# AI Agents Configuration Files

This directory contains configuration files for different AI coding assistants.

## Structure

```
ai-agents/
├── github-copilot/
│   └── copilot-instructions.md    # GitHub Copilot instructions
├── cursor/                         # Future: Cursor AI configuration
└── windsurf/                       # Future: Windsurf AI configuration
```

## Supported AI Agents

### GitHub Copilot
- **Status**: ✅ Supported
- **Configuration file**: `copilot-instructions.md`
- **Installation path**: `.github/copilot-instructions.md` (in target project)

### Future Agents

The following agents are planned for future support:

- **Cursor** - Configuration for Cursor IDE
- **Windsurf** - Configuration for Windsurf AI
- **Other agents** - Open for contributions

## How It Works

During `forge-sdd init`, the CLI prompts the user to select their preferred AI agent. The corresponding configuration file is then copied to the appropriate location in the target project.

## Adding New Agents

To add support for a new AI agent:

1. Create a new directory: `ai-agents/<agent-name>/`
2. Add configuration file(s) with appropriate instructions
3. Update `forge_sdd_cli.py` to include the new agent in the selection prompt
4. Update `pyproject.toml` and `MANIFEST.in` to include the new files
5. Document the agent in this README

## Notes

- Each agent has its own specific file structure requirements
- Configuration files are copied to the target project during initialization
- The toolkit repository itself should not have agent configurations in standard locations (like `.github/`) to avoid conflicts
