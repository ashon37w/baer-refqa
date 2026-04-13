#!/usr/bin/env bash
# Run the full BAER/REF-QA pilot pipeline end-to-end.
# Requires conda env "baer-refqa" to be active or conda to be on PATH.
set -euo pipefail
CONDA_RUN="conda run -n baer-refqa python"

echo "=== BAER/REF-QA Pilot Pipeline ==="
$CONDA_RUN scripts/bootstrap_dirs.py
$CONDA_RUN scripts/generate_pilot_data.py
$CONDA_RUN scripts/build_families.py
$CONDA_RUN scripts/generate_reference_bank.py
$CONDA_RUN scripts/generate_candidates.py
$CONDA_RUN scripts/generate_simulated_predictions.py
$CONDA_RUN scripts/run_audit.py
$CONDA_RUN scripts/aggregate_slices.py
$CONDA_RUN scripts/curate_tiers.py
$CONDA_RUN scripts/render_report.py
echo "=== Pilot complete ==="
