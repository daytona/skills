# Daytona Skill

An agent skill for creating and running sandboxes on the Daytona platform. Includes references and practical patterns for the Daytona API, CLI, Python, TypeScript, Go, and Ruby SDKs.

## Installation

### Claude Code (Plugin)

```bash
claude plugin marketplace add daytona/skills
claude plugin install daytona@daytona --scope user
```

Scope options: `user` (all projects), `project` (shared via git), `local` (gitignored).

### Manual

Clone this repository:

```bash
git clone https://github.com/daytona/skills.git
```

Copy the `daytona` subdirectory into your agent's `skills` directory:

| Agent        | Skill directory              |
| :----------- | :--------------------------- |
| Claude Code  | `~/.claude/skills/`          |
| Cursor       | `~/.cursor/skills/`          |
| OpenCode     | `~/.config/opencode/skills/` |
| OpenAI Codex | `~/.codex/skills/`           |

## Usage

The agent skill loads automatically when a request involves Daytona platform or sandbox management features. To use it manually, reference the skill directly in your prompt or code.

## Structure

```text
skills/daytona/
├── SKILL.md                # Main entrypoint
└── references/             # Reference directories
    ├── api/                # API reference documentation
    ├── platform/           # Platform reference documentation
    ├── python-sdk/         # Python SDK reference documentation
    │   ├── sync/           # Sync Python SDK reference documentation
    │   └── async/          # Async Python SDK reference documentation
    ├── typescript-sdk/     # TypeScript SDK reference documentation
    ├── go-sdk/             # Go SDK reference documentation
    ├── ruby-sdk/           # Ruby SDK reference documentation
    └── cli.md              # CLI reference documentation
```

## License

This project is licensed under the Apache License 2.0 — see [LICENSE](LICENSE) for details.
