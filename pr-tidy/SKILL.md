---
name: pr-tidy
description: Use before opening or updating a pull request, after a refactor, rename, removal, or design change, or when asked to tidy, clean up, or sweep a branch. Finds what the diff left behind — stale references and old-design wording, new behaviour without tests or docs, checkers not wired into the validator or CI or that pass silently, and numbers or examples that no longer match their source — fixes the factual ones, flags the rest, and reports both with evidence.
---

# PR tidy

A consistency sweep of a branch before it becomes a pull request. It looks at what the diff changed, then at everything the diff should have changed too.

Work on the branch's own changes. Leave untouched debt elsewhere in the repo alone unless the diff makes it wrong.

## 0. Scope

1. Read the repository's instructions first: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING*`, `README*`, and any docs they point to.
2. Find the base and the diff:

   ```bash
   base=$(git merge-base origin/main HEAD)   # or the repo's default branch
   git log --oneline "$base"..HEAD
   git diff --stat "$base"...HEAD
   git diff --name-only "$base"...HEAD
   ```

3. Check the working tree (`git status`). Keep uncommitted changes. If an edit you'd make overlaps them, stop and ask.
4. If you're on the default branch with nothing to compare, stop and say so.

## 1. Classify the diff

Sort the changes into:

- **New:** files, commands, functions, options, flags, config keys, environment variables, scripts, skills.
- **Changed:** behaviour, defaults, APIs, signatures, rules, and *design*: a guide or spec that now says something different.
- **Removed or renamed:** anything deleted, renamed, moved, or replaced.
- **Infrastructure:** build, CI, tests, tooling.

From that, list the **surface**: every name, path, flag, option, term, and rule a reader or another file could refer to. For design changes, list the old idea's key phrases too, not only its name (a removed "per-level check" may still be described as "a check under each level").

## 2. Stale references

For every removed, renamed, or redesigned item, search the whole repository, not just the changed files:

```bash
git grep -n -w "old_name"          # names, paths, flags
git grep -n -i "phrase from the old design"
```

Look in code, comments, tests, docs, READMEs, examples, notebooks, templates, skill files, diagrams (Mermaid and ASCII), and config. Every hit is either updated, or flagged with a reason.

Then build a **coverage map** for each new or changed item: where is it documented?

```
Coverage map:
  item              reference   how-to   example   explanation
  --new-flag        README      -        -         -
  check_levels.py   scripts/    -        -         -
```

An item with no coverage is a gap; report it. Don't write whole new docs pages unasked.

## 3. Tests and docs for new behaviour

For each new or changed behaviour:

- **A test** exercises it, at the layer that owns it, and its failure path where that changed. Prefer the repository's existing test pattern and the narrowest test that would catch the regression.
- **Docs** describe it wherever the old behaviour was described: reference, examples, and any guide that taught the old way.
- Report a missing test only when you can name the concrete failure it would catch. Skip speculation and untouched coverage debt.

## 4. Checkers fail loudly

For each new or changed checker, linter, validator, or check script:

1. **Wired in.** Find every entry point the repository uses: `.pre-commit-config.yaml`, `.github/workflows/*`, `Makefile`, `justfile`, `noxfile.py`, `tox.ini`, `pyproject.toml` or `package.json` scripts, and any validator that calls other checks. Confirm the checker is called from at least one. If not, wire it in the same way its siblings are, or flag it.
2. **Fails on bad input.** Run it on a deliberately broken input; it must exit non-zero.
3. **Fails on nothing.** Run it on empty or missing input (no files, no matches, nothing parsed); it must exit non-zero or say clearly that it checked nothing, never pass silently.
4. **Has a test** covering 2 and 3.

To keep this true later, add a wiring test such as [`references/test_checkers_wired.py`](references/test_checkers_wired.py).

## 5. Numbers, versions, and examples

List every number, version, date, URL, citation, command, and code example in the files the diff touched or the docs that describe them. For each:

- **Name its source:** the code or command that produces it, a config value, a dataset, or a paper with its exact version (arXiv `v3`, a DOI).
- **Re-check it:** re-run the command or re-read the source. Fix it, or flag it if you can't check.
- **Keep its condition with it:** the dataset, setting, machine, or time a number holds for ("N points in T hours on machine M", not "N points").
- **Pin external sources** to a version.
- Numbers that will keep changing are better generated from code (for example with `cog`, checked by `cog --check`) than typed by hand; suggest it.

## 6. Fix or flag

Edit minimally, in the file's own voice, structure, and terminology. Read a file fully before editing it.

**Fix without asking:**

- factual corrections that follow directly from the diff;
- stale names, paths, counts, versions, and cross-references;
- adding a new item to an existing table or list;
- wiring a checker in where its siblings show the pattern.

**Flag, or ask before changing:**

- narrative, design, or policy text, and anything that contradicts the branch's apparent intent;
- removals and large rewrites;
- security-sensitive changes;
- `CHANGELOG` entries and version bumps;
- files another person or team owns;
- new tests that need a design decision.

**Never:** rewrite or regenerate existing changelog entries, bump a version silently, hand-edit generated files (use their generator), or paste secrets or real credentials.

## 7. Verify with evidence

No claim without fresh evidence from this session, after the last relevant edit:

1. Name the command that proves the claim.
2. Run it in full.
3. Read the whole output and the exit code.
4. State the result with that evidence, or state the actual status.

Run what the repository already has: its tests, linters, `pre-commit run --all-files`, docs build, and link checks. A tool that isn't installed or a service that's down is a **verification gap**, reported as such, never a pass. "Should pass" and an agent's "done" are not evidence.

## 8. Report

```text
Scope: <base>..HEAD, N files, M commits

Changed
- path:line — what changed, and why the diff required it

Flagged (not fixed)
- path:line — the problem, why it wasn't fixed, the suggested fix

Coverage gaps
- item — where it should be documented or tested

Verified
- `command` → result (exit code)

Not verified
- what, and why (missing tool, external service, needs a decision)
```

## The mechanical layer

Most of sections 2–5 needs judgment, but some of it can run on every commit. For a repository without it, offer the starter config in [`references/pre-commit-config.yaml`](references/pre-commit-config.yaml): file hygiene, `ruff`, `codespell`, private-key detection, and `pytest` with `diff-cover` on push. `lychee` link checks and path-gated CI are better in a workflow than in a commit hook.

## Credits

Adapted, with changes, from MIT-licensed skills: `docs-sync` and `review-test-coverage` by Jakub Merta ([jMerta/codex-skills](https://github.com/jMerta/codex-skills)); the diff classification, coverage map, and fix-or-flag rules of `document-release` by Garry Tan ([garrytan/gstack](https://github.com/garrytan/gstack)); and the evidence rule of `verification-before-completion` by Jesse Vincent ([obra/superpowers](https://github.com/obra/superpowers)). Ideas, not text, from Anthropic's `pr-review-toolkit` agents ([anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)). Licenses: [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md).
