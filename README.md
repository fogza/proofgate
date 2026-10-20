# Proofgate

Proofgate is an Agent Skill for evidence-based completion. It adds a short, self-contained rule to a project's `AGENTS.md` and can be invoked again to check each acceptance criterion (AC) against fresh test or observed behavior results. The rule is useful even when the skill is not installed.

## Install on another machine

Install the versioned `skills/proofgate/` directory as `~/.agents/skills/proofgate/`. Codex, OpenCode, and Cursor discover that local location. For example, ask an AI agent with GitHub access to install `https://github.com/fogza/proofgate/tree/v0.1.1/skills/proofgate` there, or use Codex's `$skill-installer` with that URL and `--dest ~/.agents/skills`.

Review a skill's contents before installing or updating it. Use a release tag rather than an unpinned branch when you need reproducible behavior. A locally installed skill does not update itself when the GitHub repo changes.

## Use

- **First call in a project:** “Use `$proofgate` to install the completion rule here.” The skill checks `AGENTS.md` and adds only missing guidance.
- **Any later call:** “Use `$proofgate` to verify this task again.” The skill identifies AC from the task, reruns relevant checks, and reports current evidence. If no task is supplied, it only checks the project rule.
- **Without the skill:** agents that read the project's `AGENTS.md` still receive the minimum completion rule. They do not automatically run tests merely because the skill is referenced.

For pull requests, `skills/proofgate/assets/pr-template.md` provides an AC/evidence section. `scripts/check_pr.py` validates its structure; `assets/github-workflow.example.yml` shows how to use it in CI. Add the project's real checks and make the CI jobs required in branch protection. The checker cannot establish whether the AC list omits a requirement or whether the reported evidence is true; reviewers and actual test jobs cover those parts.

## Local validation

```sh
python3 -m unittest discover -s tests -v
python3 /path/to/skill-creator/scripts/quick_validate.py skills/proofgate
```

The second command uses Codex's bundled `skill-creator` when available.
