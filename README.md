# Sum up 13 November's world news in one image

make.fun bounty: https://make.fun/bounty/news-image-01
$250 USDC shared by the top 100 entries ($50 / $20 / $10 / $5 / $1.50).
Deadline: Sat 14 Nov 2026 20:00 UTC = Sun 15 Nov 2026 03:00 WIB.
Status: BUILT, NOT SUBMITTED. No GitHub repo created, no entry
submitted, nothing signed, nothing paid, no wallet connected.

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

## Sources (researched 15 Nov 2026, ~00:12 WIB)

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

`main.py` — Python 3.13 target, stdlib only (`os`, `struct`,
`sys`, `zlib`). No PIL, no network imports, no external files.
Text is rendered with an embedded 5x7 bitmap font; the PNG is
encoded by hand (zlib, fixed level 9, no timestamps), so output
is deterministic.

Default output is the bounty path `/output/entry.png`. An optional
positional argument or `OUTPUT_PATH` env var overrides it for
local testing only.

## Run commands (exact)

```bash
cd ~/workspace/makefun/news-image-01
python3 main.py output/run1.png
python3 main.py output/run2.png
python3 main.py            # writes /output/entry.png
```

Local Python here is 3.12.3; the code uses no 3.13-only features
and is intended for Python 3.13 as the bounty requires.

## Verification results (15 Nov 2026, ~00:15 WIB)

- run1, run2 and /output/entry.png are byte-identical:
  sha256 `b9662155d7ee7a38837c9313fee324aee1dba48cc295ea9724fd238b2d789f7a`
  (all three files, after the final layout fix; the pre-fix hash
  was ae4ff8bbfad1810fb7344940707724a321f7940fb2224c29880d819d6c1ef0a4)
- Size: 20,389 bytes (≤1 MiB) — PNG, 1024x1024 (≤1024x1024),
  valid PNG signature, IHDR 1024x1024.
- No network: `main.py` imports only `os`, `struct`, `sys`,
  `zlib`; grep found no socket/urllib/requests/http calls.
  The only `open()` is the local file write.
- Visual check: previewed `preview.png` — all 6 stories, the
  header and the footer are fully visible, no clipping.
  (First preview clipped story 06; spacing was tightened and
  re-verified before this README was written.)

## Files

- `main.py` — the entry program
- `preview.png` — copy of the generated image (20,389 bytes)
- `output/run1.png`, `output/run2.png` — the two verification runs
- `README.md` — this file

## What remains before submission (NOT done)

1. Create a public GitHub repo owned by the user's own GitHub
   account, created after the bounty opened, under an
   OSI-approved license, with `main.py` in its root.
2. Produce the AI agent session transcript for the sessions
   that built it (min 30% of lines, min 5 turns, timestamps
   within the bounty window) and upload it with the submission.
3. Get the user's approval for the make.fun agent-connect flow
   (make.fun/connect, 15-minute code) — an agent wallet cannot
   be used to log in.
4. Submit via make.fun before Sun 15 Nov 2026 03:00 WIB.
   No submission, signing, payment or wallet connection has
   been done in this build.
