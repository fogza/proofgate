---
name: proofgate
description: Add or refresh evidence-based completion rules in a project instruction file chosen by the user, or recheck a task's acceptance criteria with current evidence before reporting it complete.
---

# Proofgate

Use this skill to set up a completion rule, verify a current task, or both. On each invocation, ask the user to choose `AGENTS.md`, another file they name, or no file change before proceeding. If the user already made that choice for this invocation, do not ask again. Do not choose `AGENTS.md` by default. The no-file-change option allows Verify without setup. A written rule should be understandable without this skill.

## 1. Set up the project rule, if requested

Find the intended project root from the working directory and project context; do not assume Git exists. After the user confirms a destination, read that file and any relevant existing completion or verification rules before editing. Preserve project-specific checks and higher-priority instructions. If the user chooses no file change, continue to Verify when there is a task.

- If the rule already covers AC identification, actual evidence, honest incomplete status, and the limit of build-only checks, leave it in place. Add the skill reference only if useful; avoid a duplicate section.
- If the Proofgate marked block exists but is outdated, update that block. For `AGENTS.md`, `python3 scripts/install_rule.py --project <root> --lang en|th` can do this.
- If no equivalent rule exists, create or append the self-contained rule in the confirmed file. For `AGENTS.md`, the same script can do this. Choose `th` for a Thai file, otherwise `en`.
- If an unmarked rule partly covers the standard, edit that section narrowly to fill the gaps; do not append a second generic policy. On later calls, treat the completed section as already installed.

The templates are in `assets/rule.en.md` and `assets/rule.th.md`. Adapt their wording to the confirmed file. Do not embed an absolute local skill path in a project file. Keep the project rule short; task-specific AC belong with the task or its spec, not in a general project rule.

## 2. Verify the current task, if any

Identify the current task's AC from the user request and applicable spec. Inspect relevant project files before asking questions. Ask only when a material ambiguity prevents a pass/fail decision. If no task or AC source is available, report any setup result and ask for the task to verify.

For each AC, choose direct evidence of the requested outcome: focused tests, command results, diff or file inspection, rendered output, or observed UI behavior. Follow project-specific verification instructions. Run relevant checks **now** on every Verify invocation; a prior pass, a green build alone, or a checked box in a plan is not current proof of behavior. Avoid unrelated suites and destructive external tests. Distinguish mock data from authorized live data.

Report a compact AC-to-evidence mapping with `verified`, `incomplete`, or `blocked`. Include the check, observed result, and any untested limit. Claim the whole task complete only when every required AC is verified. Do not fabricate command output or infer UI behavior from a successful build. On repeat invocation, inspect current state and rerun relevant checks rather than reusing earlier results.
