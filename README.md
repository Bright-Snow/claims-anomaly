What it does — finds providers whose Medicare payments run high against comparable peers


What data — CMS public use file, New Jersey, 2024, ~321k rows


The four filters and what each rules out: Removed six cardiologists billing A9500 globally while peers billed professional(component only)
peer grouping (facility vs professional) 
minimum peer size, isolation (tight clusters) - Removed cardiology & electrophysiology cluster
max_gap (split billing modes) - Removed A9500 & A9502

What it does not claim — billing anomalies, not fraud
