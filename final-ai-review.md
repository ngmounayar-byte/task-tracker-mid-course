# Final AI Review and Ownership Evidence

## AGENTS.md guardrails
- Repo-specific stack and commands included: **yes**.
- Docs-first/read-first guardrail included: **yes**.
- Unexpected `app/` / `frontend/` edits rule included: **yes**.
- Secret/data handling rule included: **yes**.
- CI failure-hiding shortcuts prohibited: **yes**.

## AI code review mini-log

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| Keep pytest isolated from `app/data/tasks.json` by using `TASKS_FILE` and a separate test file. | Useful | The mid-course baseline showed tests could wipe the seed data when test and app storage were the same file. | Kept the existing isolation design and re-ran the full suite: 36 passed. |
| Treat an explicit `tags: null` update as safe input without tracing the response/storage model. | Wrong | The existing prompt log records that passing `None` through could corrupt a non-optional `list[str]` field because `model_copy()` does not revalidate in that path. | The generated behavior was corrected so explicit null clears tags to `[]` rather than persisting `None`. |
| Add Docker/CI by changing application feature code at the same time. | Noise | The final-project brief is about release readiness and specifically protects `app/` and `frontend/` from unrelated changes. | Rejected. Final additions are configuration/documentation only; no final feature change was made. |

## AI security mini-review

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| Real `.env` files could leak secrets if copied into an image or committed. | `.gitignore`, `.dockerignore`, `.env.example` | Valid | Secret-bearing environment files should not be committed or baked into Docker. | `.env`/`.env.*` are ignored; keep only the non-secret `.env.example`. |
| CI may hide test failures. | `.github/workflows/ci.yml` | False Positive | The workflow has no `continue-on-error`, no `|| true`, and directly runs pytest. | No change; confirm the hosted run is green after push. |
| Application code may execute shell commands or dynamic `eval`/`exec`. | repository-wide manual pattern scan on 2026-09-02 | Noise | No `eval(`, `exec(`, `os.system`, `subprocess`, `shell=True`, or similar pattern was found in project code. | No action required unless future code introduces these patterns. |

## Manual security check
I manually checked the repository for common secret names and dangerous execution patterns rather than relying only on an AI summary. `.env.example` contains only `PORT=8000` and `APP_ENV=development`, and the project ignore rules exclude real `.env` files. I also found no shell-execution or dynamic-code-execution patterns in the application files. This matters because the final release evidence should not claim security based only on generated text; the repository itself was inspected.

## One AI output I rejected or corrected
During the tags work, an AI-generated first pass allowed `TaskUpdate.tags` to remain `None` when a client explicitly sent `tags: null`. Reviewing the downstream model/storage behavior showed that this could put `None` into a field that is supposed to be a list and later cause validation failure. I did not accept that output as-is. The behavior was corrected so explicit null clears tags to an empty list, and the full test suite remains green.

## Three AI usage rules
1. Never paste: credentials, tokens, real `.env` values, production logs, or real customer/patient/personal data.
2. Always verify: inspect the diff and run the relevant command or test before treating AI output as correct.
3. Record AI contributions by: naming the file/decision, grading important findings, and documenting corrections or rejected suggestions.

## Ownership statement
I am comfortable submitting this repository because I can explain the application structure, the two mid-course features, the tests, and the final release-readiness files. AI was used to draft and review parts of the work, but its output was not accepted automatically: findings were checked against files and commands, and at least one generated behavior was corrected after review. I re-ran the full test suite and verified the local `/health` endpoint myself during the final packaging check. Where this environment could not provide real evidence, such as a hosted GitHub Actions URL or a Docker runtime result, I left an explicit completion note rather than claiming a result that was not observed.
