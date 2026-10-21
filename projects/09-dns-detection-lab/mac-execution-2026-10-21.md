# Project 09 — Owner-Mac execution record — 2026-10-21

## Evidence basis and provenance

This is a screenshot-reviewed summary of the owner's local Mac execution of the offline synthetic DNS lab. It is not a raw execution transcript or a claim that the assistant performed the owner's run. Two screenshots available from the prior conversation were reviewed for the metadata, test outcome and comparison-success message below. The detector counts and alert details are carried forward from the owner's supplied summary of earlier screenshot review; those earlier detector-output screenshots were not available for reinspection during this finalization.

Original raw logs, generated outputs and screenshots remain on the owner's Mac and are **not uploaded to this GitHub repository or PR**. Screenshots were shared in conversation for review. This public record deliberately omits the terminal username, computer hostname and personal filesystem paths. No raw system or network logs are included.

## Recorded environment

- Executed source commit: `f1853846254cd1aab3613f85033b0df3adeda074`
- Source branch: `project-09-dns-detection-lab`
- Python: `3.9.6`
- Recorded run date/time: `Wed 21 Oct 2026 17:48:29 UTC` (`2026-10-21T17:48:29Z`)
- Platform: owner's Mac; exact macOS version was not established.
- The timestamp is saved run metadata shown in the screenshot, not independently verified start/end timing.

The evidence applies to the source commit above. This execution record and subsequent documentation updates were added after that run.

## Results

| Item | Recorded outcome | Evidence basis |
| --- | --- | --- |
| Unit tests | 10 of 10 passed; `Ran 10 tests in 0.010s`, followed by `OK` | Direct screenshot review |
| Reference comparison | Screenshot displays `SUCCESS: Project 09 alerts match expected results!`; owner reports generated JSON exactly matched committed reference JSON | Screenshot success message plus owner summary; raw JSON not inspected |
| Input | 628 lines; 627 unique events; 1 duplicate | Owner-supplied summary of earlier screenshot review |
| Alerts | Exactly one Medium alert for fictional client `10.20.5.7` | Owner-supplied summary of earlier screenshot review |
| Alert counts | 450 TXT queries and 450 distinct names | Owner-supplied summary of earlier screenshot review |

The ten displayed passing tests cover inclusive thresholds, 99-query and 79-distinct-name non-alert cases, event-ID deduplication, invalid lines, response/A-record exclusions, exclusive window end, UTC offset normalization, unrelated-domain exclusion and input ordering.

The committed reference places the fictional alert in `[2026-10-15 08:30:00, 08:35:00) UTC` for `sync.example`. This is the synthetic event window, distinct from the October 21 execution date. Reference data is not relabeled as an owner-generated artifact.

## Interpretation and limits

The run demonstrates local execution of a standalone Python detector and its tests on fabricated DNS records. The combined volume and distinct-name thresholds identify a suspicious synthetic TXT burst; volume alone would also include repetitive benign-looking controls.

This does not establish DNS tunneling, exfiltration, compromise, process attribution or any real-world incident. It does not demonstrate live DNS collection, production telemetry, SIEM ingestion, a deployed SIEM rule or production SIEM work. Fixed windows, illustrative thresholds and first-occurrence deduplication remain documented limitations.

The separately proposed milestone of ingestion and rule validation in an authorized isolated SIEM remains incomplete. Public readers can reproduce the synthetic lab, but cannot independently audit the owner's raw Mac transcript from this summary alone.
