# ChatGPT ↔ Hermes handoff protocol

## State and authority

This is GitHub-based asynchronous coordination, NOT an implemented A2A protocol server, live agent connection, or background ChatGPT listener. ChatGPT works when invoked in this conversation. Hermes must explicitly fetch the repository during its own task. No credentials belong in commits, logs, prompts or handoffs.

User instruction: save accepted preview, connect portfolio repository references, DO NOT PUBLISH. No deployment, release, Pages change, domain change, production merge or production modification is authorized by this handoff. Do not add automatic publication workflows. Do not touch OmniGuard repositories.

## Work cycle

1. Fetch current remote state; inspect repository instructions and collaboration/tasks.json. Never reset or overwrite uncommitted local work.
2. Claim one task in your own branch: owner, state, base commit, touched paths. Push claim; verify latest remote state before proceeding. Simultaneous claims require resolution, not last-writer-wins. This is a convention, not a distributed lock.
3. Work on a task branch; keep approved preview intact unless the assigned task explicitly changes it. Do not transplant code across repositories without inspecting licenses and integration requirements.
4. Commit changes and add a handoff in collaboration/handoffs/<task-id>-<agent>.md with base/head SHAs, files changed, commands actually executed, results, limits and next action.
5. Open a draft PR for review. Reviewer inspects the actual diff and test evidence. Preserve other agents' work; resolve conflicts explicitly. Never force-push shared branches.
6. Distinguish code saved, checks passed, browser verified, service connected and deployed. None implies the others. Publication requires explicit new user approval.

## Roles

ChatGPT: design/code review, task definition and scoped repository edits during an active user session.
Hermes: local build/runtime checks, browser desktop/mobile QA, evidence capture and implementation on assigned branches.
Emir: product direction and production publication approval.

## Future live A2A (proposed, not installed)

A separately authenticated Hermes service could expose bounded task submission/status/artifact endpoints through a supported connector. It needs persistent hosting, scoped authentication, idempotent task IDs, audit logs and approval enforcement. No public shell endpoint, shared personal token or unauthenticated webhook. GitHub handoffs work first without this infrastructure.
