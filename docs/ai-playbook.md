# My AI Playbook

## When I reach for AI first
I use AI first when I need to understand an unfamiliar part of the repo, turn a requirement into a small implementation plan, draft focused tests, review a diff, or check release configuration such as CI and Docker. It was especially useful in this project for tracing behavior across the route, service, repository, and model layers and for suggesting edge cases I might otherwise miss.

## When I do not reach for AI first
I do not start with AI when the main goal is for me to learn the code by reading it, when important project context is missing, or when the task involves credentials, private data, production logs, or other information that should not be pasted into a tool. I also do not let AI decide product scope for me; I first compare the request with the course brief and the existing application.

## My non-negotiables
I never paste real secrets or personal/customer data. I do not weaken tests or CI to obtain a green result. I inspect generated changes before keeping them, and I run a real verification command for claims that can be tested. If I cannot explain a changed line, command, configuration choice, or AI suggestion, I do not treat it as final work.

## My review rules
For code, I read the affected files, inspect the diff, run the narrow relevant tests, then run the complete pytest suite. For documentation, I compare commands, endpoints, and behavior with the actual repo or running app. For AI review/security findings, I grade them instead of accepting every comment: useful findings get verified and acted on; false positives/noise are recorded or rejected with a reason. I also keep an eye on whether an AI suggestion quietly expands scope.

## What I am still figuring out
I am still learning how much AI-generated infrastructure is appropriate before it becomes harder to understand than writing the configuration myself. I also want clearer team norms for which AI interactions should be recorded in routine development versus only for higher-risk or release-related work.

## Decision Card
- **New feature:** read the requirement and existing architecture first; ask AI for options only after scope is clear.
- **Code review:** let AI identify risks, then verify each important comment in the actual diff/tests.
- **Debugging:** reproduce the problem first and give AI the smallest safe context needed.
- **Infrastructure:** require exact commands and verify them locally or in CI; never claim an unobserved run.
- **Never paste:** secrets, tokens, production `.env` values, real patient/customer data, or sensitive logs.
- **One rule:** AI can suggest; I still have to understand, verify, and own the result.
