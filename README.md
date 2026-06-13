# YC Application Tracker

A simple tracker that lists hand-picked Y Combinator startups (US, small teams,
actively hiring, recent batches) matched to my resume, with a personalized
application message per role, the YC company-page link, an "Applied" checkbox,
and a "why not applied" notes field.

## Run locally (with on-disk persistence)
```bash
python3 server.py
# open http://localhost:8765/
```
State is saved to `tracker_data.json` (gitignored). `companies_master.json`
tracks every company already proposed, so future batches never repeat one.

## Hosted (Vercel)
The hosted build is the static `index.html`. On Vercel there is no writable
filesystem, so checkbox/notes state is kept in the browser's localStorage.
