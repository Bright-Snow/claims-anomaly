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

**Isolation** — compare each provider to the 90th percentile of its own
peer group, not the median. Removed five cardiologists on 78431 whose
ratios sat within 0.5% of each other; five people billing identically
is a broken baseline, not five outliers. 

**Max gap** — largest jump between sorted neighbours in a peer group.
On A9500, payments climbed smoothly from $32 to $277, then jumped to
$1,088 with nothing between. That gap is two billing modes — global
versus professional-component-only — not one distribution with a tail.
Removed six cardiologists that isolation had missed.

## What this is not fraud, but billing anomalies.
