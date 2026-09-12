# GitHub Actions deployment

## Repository secrets

Add these values under repository **Settings → Secrets and variables →
Actions**:

- `TELEGRAM_BOT_TOKEN` — Telegram bot token;
- `TELEGRAM_CHAT_ID` — target channel or chat identifier.

Do not add a fine-grained GitHub token to this repository. GitHub Actions uses
its short-lived built-in `GITHUB_TOKEN` to commit `storage/published.json`.

## Control run

Open **Actions → Pets Autoposter → Run workflow** and leave **Send selected
posts to Telegram** disabled. This runs tests and the complete collection,
selection, extraction, formatting, and image-validation pipeline without
calling Telegram or changing publication history.

Enable the switch only for an explicitly approved live control publication.

## External cron

The scheduler calls the `workflow_dispatch` endpoint for
`.github/workflows/autoposter.yml`. Store its fine-grained personal access token
in the scheduler, never in the repository or request URL. Scope the token to
this repository only and grant the minimum Actions permission required to run
workflows.

For a live scheduled run, send the workflow input `publish` with value `true`.
Omitting the input or setting it to `false` produces a DRY_RUN.

The workflow serializes runs, executes the test suite first, and records
publication history only after confirmed Telegram success. Repository workflow
permissions must allow Actions to write contents so the history commit can be
pushed.
