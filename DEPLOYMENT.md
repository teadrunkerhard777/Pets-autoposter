# GitHub Actions deployment

## Repository secrets

Add these values under repository **Settings → Secrets and variables →
Actions**:

- `TELEGRAM_BOT_TOKEN` — Telegram bot token;
- `TELEGRAM_CHAT_ID` — target channel or chat identifier.
- `PEXELS_API_KEY` — free API key used by the separate video schedule.

Do not add a fine-grained GitHub token to this repository. GitHub Actions uses
its short-lived built-in `GITHUB_TOKEN` to commit `storage/published.json`.

## Control run

Open **Actions → Pets Autoposter → Run workflow** and leave **Send selected
posts to Telegram** disabled. This runs tests and the complete collection,
selection, extraction, formatting, and image-validation pipeline without
calling Telegram or changing publication history.

Enable the switch only for an explicitly approved live control publication.

## External cron

Create a fine-grained personal access token with:

- repository access: **Only select repositories → Pets-autoposter**;
- repository permission: **Actions → Read and write**;
- the shortest practical expiration period.

Store this token in the scheduler, never in the repository or request URL.

For cron-job.org or another HTTP scheduler, create a job with these values:

- method: `POST`;
- URL: `https://api.github.com/repos/teadrunkerhard777/Pets-autoposter/actions/workflows/autoposter.yml/dispatches`;
- header `Accept`: `application/vnd.github+json`;
- header `Authorization`: `Bearer YOUR_FINE_GRAINED_TOKEN`;
- header `X-GitHub-Api-Version`: `2026-03-10`;
- header `Content-Type`: `application/json`;
- request body: `{"ref":"main","inputs":{"publish":true}}`.

Choose the scheduler timezone explicitly. Do not schedule runs closer together
than the maximum expected workflow duration; GitHub also serializes them with
the `pets-autoposter` concurrency group.

Before enabling the recurring job, send the same request once with
`"publish":false`. It must start a green DRY_RUN and must not create a Telegram
message or change `storage/published.json`. After that check, perform one manual
live run from the GitHub Actions page before changing the cron body to
`"publish":true`.

GitHub returns a successful response for an accepted dispatch. The new run then
appears under the repository's **Actions** tab; the dispatch response does not
mean that the workflow itself has already completed.

The workflow serializes runs, executes the test suite first, and records
publication history only after confirmed Telegram success. Repository workflow
permissions must allow Actions to write contents so the history commit can be
pushed.

## Video schedule

The `Pets Video Autoposter` workflow runs at 13:00 and 20:00 in
Asia/Yekaterinburg (08:00 and 15:00 UTC). Each run selects and sends at most one
unpublished vertical Pexels video. If no suitable new video is available, it
publishes nothing.

Create a free Pexels API key and store it as the `PEXELS_API_KEY` repository
secret. Before relying on the schedule, open **Actions → Pets Video
Autoposter → Run workflow** with publication disabled. After that DRY_RUN is
green, perform one manual live run with publication enabled. Scheduled runs are
live; manual runs remain safe by default.
