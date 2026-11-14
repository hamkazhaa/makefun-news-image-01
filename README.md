# Sum up 13 November's world news in one image

make.fun bounty: https://make.fun/bounty/news-image-01
$250 USDC shared by the top 100 entries ($50 / $20 / $10 / $5 / $1.50).
Deadline: Sat 14 Nov 2026 20:00 UTC = Sun 15 Nov 2026 03:00 WIB.
Status: REBUILT IN A FRESH SESSION 2026-11-15 ~01:56 WIB, NOT
SUBMITTED, NOT PUSHED. Nothing signed, nothing paid, no wallet
connected in this rebuild. The repo already contains
`.makefun/owner.json` (commit 071e9208) from the earlier fix for
the "Repository owner failed" check.

## What the image shows

1024x1024 PNG, "WORLD NEWS — FRIDAY 13 NOVEMBER 2026",
six numbered stories:

1. **Ukraine launches huge drone attack** — Kyiv said it fired
   almost 1,200 drones at Russia overnight, one of its biggest
   strikes of the war, as US-led talks widen to include Europe.
2. **US says it downed Iranian drones** — Washington said it shot
   down two Iranian drones headed for Bahrain. Tehran claimed it
   hit a US radar there. That claim could not be verified.
3. **Microsoft 365 outage hits day 2** — Outlook, Teams and
   Copilot were still being restored after a global outage that
   began on 12 November and spread across more than 70 countries.
4. **Nvidia chief Jensen Huang resigns** — Huang quit as chief
   executive after reports of an affair and links to a woman
   alleged to be a Chinese spy. He was summoned to testify
   to Congress.
5. **FAA lifts US flight ground stop** — US flights resumed on
   Friday evening after a communications failure halted
   departures nationwide for more than four hours.
6. **Qatar and Turkey sign defence pact** — Doha and Ankara signed
   a mutual defence deal in Istanbul, pledging a united stance
   against an outside armed attack.

Footer: "Sources: Associated Press, Reuters, Guardian, BBC —
13 Nov 2026. Summary image, not a photo. Claims are labelled
as claims."

## Sources (researched 14-15 Nov 2026)

- https://levelheadlines.com/briefs/2026-11-13/ — Ukraine ~1,200
  drones (AP), US downed two Iranian drones headed for Bahrain,
  Iran radar claim, Microsoft 365 outage day 2.
- https://www.theraisinapost.com/24-hours/world-news/2026-11-13/
  — Taiwan/China drills, IEA oil outlook, US chip-control dispute.
- https://zarknews.com/zark-news-daily-briefing-november-13-2026/
  — Iran radar claim (unverified), Europe joining Ukraine talks,
  Binance-hack seizure, Pope Leo in Peru.
- https://www.profilenews.com/en/november-13-2026-world-news/
  — FAA lifted the ground stop Friday evening; Microsoft
  restoring services; Qatar-Turkey defence agreement; IAEA
  concern over Iran's Isfahan plant.
- https://michaelbrunger.com/briefs/2026-11-13/ — Nvidia CEO
  Jensen Huang resigned (Guardian/BBC), summoned to Congress;
  Microsoft outage; Ukraine drone hit on a Russian warship.
- https://make.fun/bounty/news-image-01 — bounty brief itself
  (verified 14 Nov 2026 17:12 UTC): $250, ends 20:00 UTC,
  program at main.py (Python 3.13) or main.ts, writes
  /output/entry.png, PNG/JPEG ≤1 MiB, ≤1024x1024, no network,
  two runs byte-identical, max 10 entries/day, 20 total.

No news was invented. Where a claim could not be independently
verified (Iran's radar claim), the image labels it as a claim.

## Program

`main.py` — Python stdlib only (`os`, `struct`, `sys`, `zlib`).
No PIL, no network imports, no external files. Text is rendered
with an embedded 5x7 bitmap font; the PNG is encoded by hand
(zlib, fixed level 9, no timestamps), so output is deterministic.

Default output is the bounty path `/output/entry.png`. An optional
positional argument or `OUTPUT_PATH` env var overrides it for
local testing only.

## Run commands (exact)

```bash
cd ~/workspace/makefun/news-image-01-repo
python3 main.py /tmp/rebuild/v3-run1.png
python3 main.py /tmp/rebuild/v3-run2.png
python3 main.py            # writes /output/entry.png
```

Local Python here is 3.12.3; the code uses no 3.13-only features
and is intended for Python 3.13 as the bounty requires.

## Verification results

### Original program (15 Nov 2026, ~00:15 WIB, before this rebuild)

- run1, run2 and /output/entry.png byte-identical:
  sha256 `b9662155d7ee7a38837c9313fee324aee1dba48cc295ea9724fd238b2d789f7a`
- Size: 20,389 bytes, PNG, 1024x1024.
- Re-verified at the start of this rebuild session
  (2026-11-14T18:56:36Z): two fresh runs in
  `~/workspace/makefun/news-image-01-repo` produced the same
  20,389 bytes and the same sha256
  `b9662155d7ee7a38837c9313fee324aee1dba48cc295ea9724fd238b2d789f7a`,
  byte-identical to the committed `preview.png`.

### Rebuilt program (this session, 2026-11-15 ~01:56-01:57 WIB)

- `main.py` was written fresh in this session
  (`muse.write`, 11,807 bytes), then revised a second time
  (`muse.edit` x3): body line height 21 px -> 23 px (2 px gap
  between 21 px glyphs), story start y 196 -> 192, post-body
  gap 8 -> 6 px, divider gap 10 -> 8 px.
- First rebuilt runs (v2): 20,303 bytes, 1024x1024,
  sha256 `296ca995d6c4275cb2178615a3fa786115971edd8728fc717127530585478979`,
  byte-identical across two runs. Preview showed all 6 stories,
  header and footer fully visible with no clipping, but body
  lines were touching (no leading) — that is what the second
  revision fixed.
- Final rebuilt runs (v3, after the spacing revision):
  run1 and run2 byte-identical:
  sha256 `330320b11722e674a5d4c50c625a7873fab48acdbbc76de58a274052e8960466`
- Size: 20,411 bytes (≤1 MiB) — PNG, 1024x1024 (≤1024x1024),
  valid PNG signature, IHDR 1024x1024.
- `preview.png` in this repo was updated to the final v3 output
  (same sha256 `330320b11722e674a5d4c50c625a7873fab48acdbbc76de58a274052e8960466`).
- No network: `main.py` imports only `os`, `struct`, `sys`,
  `zlib`; checked in this session — no socket/urllib/requests/
  http calls. The only `open()` is the local file write.
- Visual check: previewed the final `v3-run1.png` — all 6
  stories, the header and the footer are fully visible, body
  lines now have a clear gap, no clipping. Story 06 ends well
  above the footer band.

## Files

- `main.py` — the entry program (rebuilt in this session)
- `preview.png` — copy of the final rebuilt image (20,411 bytes)
- `README.md` — this file
- `.makefun/owner.json` — `{"wallet": "FxmXf1NPQE1YyVZYZAEPoDxVzw1YSxRGYAzcmMNQZ3s"}`
  (commit 071e9208, already in the repo before this rebuild)

## What remains before submission (NOT done in this rebuild)

1. Commit the rebuilt `main.py`, `preview.png` and this
   `README.md` to the repo (new commit SHA — the submission
   must use that new SHA, not 071e9208).
2. Produce the AI agent session transcript for the sessions
   that built it (min 30% of lines, min 5 turns, timestamps
   within the bounty window) and upload it with the submission.
3. Submit via make.fun as @hamka before Sun 15 Nov 2026
   03:00 WIB, with the user signing in Phantom.
   No submission, signing, payment or wallet connection has
   been done in this rebuild.
