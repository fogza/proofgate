---
name: proofgate
description: Install or refresh evidence-based completion rules in a project's AGENTS.md, or recheck a task's acceptance criteria with current test results before reporting it complete.
---

# Proofgate

Use this skill in two modes. **Setup** installs the project rule. **Verify** checks a current task. Every invocation starts with setup; if there is no task to verify, stop after setup and report what changed. The rule in `AGENTS.md` remains useful when this skill is unavailable.

## 1. Ensure the project rule

Find the intended project root from the working directory and project context; do not assume Git exists. Read its `AGENTS.md` and any existing completion or verification rules before editing. Preserve project-specific checks and higher-priority instructions.

- If the rule already covers AC identification, actual evidence, honest incomplete status, and the limit of build-only checks, leave it in place. Add the skill reference only if useful; avoid a duplicate section.
- If the Proofgate marked block exists but is outdated, run `python3 scripts/install_rule.py --project <root> --lang en|th` from this skill directory. The command updates only that block.
- If no equivalent rule exists, use the same command to create or append the self-contained rule. Choose `th` for a Thai `AGENTS.md`, otherwise `en`.
- If an unmarked rule partly covers the standard, edit that section narrowly to fill the gaps; do not append a second generic policy. On later calls, treat the completed section as already installed.

The templates are in `assets/rule.en.md` and `assets/rule.th.md`. Do not embed an absolute local skill path in a project file. Keep the project rule short; task-specific AC belong in the task, issue, plan, or PR, not in `AGENTS.md`.

## 2. Verify the current task, if any

Identify the current task's AC from the user request and applicable spec. Inspect relevant project files before asking questions. Ask only when a material ambiguity prevents a pass/fail decision. If no task or AC source is available, report that setup is complete and ask for the task to verify.

For each AC, choose direct evidence of the requested outcome: focused tests, command results, diff or file inspection, rendered output, or observed UI behavior. Follow project-specific verification instructions. Run relevant checks **now** on every Verify invocation; a prior pass, a green build alone, or a checked box in a plan is not current proof of behavior. Avoid unrelated suites and destructive external tests. Distinguish mock data from authorized live data.

Report a compact AC-to-evidence mapping with `verified`, `incomplete`, or `blocked`. Include the check, observed result, and any untested limit. Claim the whole task complete only when every required AC is verified. Do not fabricate command output or infer UI behavior from a successful build. On repeat invocation, inspect current state and rerun relevant checks rather than reusing earlier results.

## 3. Projects using pull requests

For a GitHub PR workflow, use `assets/pr-template.md` as the AC/evidence section and `scripts/check_pr.py` as a structural CI check. Add relevant project test commands as separate CI steps or required jobs. Configure the resulting status check as required before merging; without branch protection, a green workflow is advisory. A human reviewer must compare the AC list with the originating request because a structural check cannot detect omitted requirements. If a project has no Git or PR workflow, use the local Verify report.
