# claims-anomaly

Finds Medicare providers whose payments run high compared to
genuinely comparable peers.

## Data

CMS Medicare Physician & Other Practitioners public use file,
New Jersey, 2024. ~321,000 rows.

## Why four filters

Naive outlier detection on this data returns almost entirely
false positives. Each filter removes one class:

**Peer grouping** — compare within provider type, not across all
providers. Ambulatory surgical centers are paid on a different
schedule than physicians; without this, eleven of the top fifteen
results were ASCs billing normally.

**Minimum peer size** — groups under 20 providers don't have a
meaningful median.

**Isolation** — Removed cardiology & electrophysiology cluster(billed globally & professional-component-only), and ASC. 

**Max gap** — Removed A9500 & A9502 (dragging average)

## What this is not fraud, but billing anomalies.

...
