# Proofgate

Proofgate is an Agent Skill for evidence-based completion. Use `init` to add a short, self-contained rule to a project file you choose, or invoke the skill without `init` to check each acceptance criterion (AC) against fresh test or observed behavior results. The written rule remains useful when the skill is not installed, provided the agent reads the chosen file.

## Install on another machine

Install the versioned `skills/proofgate/` directory as `~/.agents/skills/proofgate/`. Codex, OpenCode, and Cursor discover that local location. For example, ask an AI agent with GitHub access to install `https://github.com/fogza/proofgate/tree/v0.1.2/skills/proofgate` there, or use Codex's `$skill-installer` with that URL and `--dest ~/.agents/skills`.

For a fresh manual install:

```sh
git clone --depth 1 --branch v0.1.2 https://github.com/fogza/proofgate.git /tmp/proofgate-v0.1.2
mkdir -p ~/.agents/skills
cp -R /tmp/proofgate-v0.1.2/skills/proofgate ~/.agents/skills/proofgate
```

Review a skill's contents before installing or updating it. Use a release tag rather than an unpinned branch when you need reproducible behavior. A locally installed skill does not update itself when the GitHub repo changes.

## Use

- **Set up a project rule:** “Use `$proofgate init` in this project.” The skill asks whether to use `AGENTS.md` (the suggested default), another named file, or no file change. It waits for your choice, then fills only missing guidance in the selected file.
- **Verify a task:** “Use `$proofgate` to verify this task.” The skill identifies AC from the task, reruns relevant checks, and reports current evidence without asking for a file or changing one. If no task is supplied, it asks what to verify.
- **Set up and verify together:** “Use `$proofgate init` and verify this task.” The skill sets up the rule after your file choice, then checks the task.
- **Without the skill:** the rule still applies when an agent reads the file you chose. Referring to the skill in that file does not itself run tests.

These examples use Codex's `$skill` syntax. Other providers may use different ways to invoke an installed skill; `init` is part of the request, not a terminal command.

## Local validation

```sh
python3 -m unittest discover -s tests -v
python3 /path/to/skill-creator/scripts/quick_validate.py skills/proofgate
```

The second command uses Codex's bundled `skill-creator` when available.
