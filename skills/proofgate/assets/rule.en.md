<!-- proofgate:start v1 -->
## Completion evidence (Proofgate)

- Before implementation, identify acceptance criteria (AC) from the request or applicable spec. Clarify only material gaps that prevent deciding whether an outcome passes.
- Before marking work complete, compare every required AC with results observed in the current work session. State `verified`, `incomplete`, or `blocked` for each, with the check performed, actual result, and any limit. Do not claim the whole task complete while a required AC is unverified.
- Run checks relevant to the change and inspect user-visible behavior when it matters. A passing build or a checked plan item alone does not prove behavior. Never invent test results; report checks that could not be run.
- Use the `proofgate` skill for setup or a fresh verification pass when available (https://github.com/fogza/proofgate). These rules still apply without the skill.
<!-- proofgate:end -->
