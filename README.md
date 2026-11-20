# skills

Agent skills I use across my repositories. Each folder is one skill in the open `SKILL.md` format, which Claude Code, Codex, Cursor, and other agents read.

| Skill | What it does |
|---|---|
| [`pr-tidy`](pr-tidy/SKILL.md) | A consistency sweep before a pull request: stale references and old-design wording, tests and docs for new behaviour, checkers wired in and failing loudly, numbers and examples re-checked against their sources, and a blocking check for personal information and credentials. Includes a starter pre-commit config. |

## Install

With the [`skills`](https://github.com/vercel-labs/skills) CLI, which installs into whichever agents you have:

```bash
npx skills add chiuhoward/skills
```

Or clone and link, so `git pull` updates every agent at once:

```bash
git clone https://github.com/chiuhoward/skills.git
cd skills && ./install.sh
```

`install.sh` links each skill folder into `~/.agents/skills/` and `~/.claude/skills/`, and can be re-run after adding a skill.

## License

MIT, except where a skill credits adapted work; see [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
