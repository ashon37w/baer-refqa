# BAER / REF-QA

**Audit-first benchmark for spoken counterfactual QA** — measures when text is sufficient and when audio contributes irreplaceable information.

## Quickstart

### 1. Setup Environment

```bash
conda env create --file environment.yml
conda activate baer-refqa
```

### 2. Run Full Pilot Pipeline

```bash
# Step 1: Generate synthetic pilot data (300 samples)
conda run -n baer-refqa python scripts/generate_pilot_data.py

# Step 2: Build semantic families
conda run -n baer-refqa python scripts/build_families.py

# Step 3: Generate reference bank
conda run -n baer-refqa python scripts/generate_reference_bank.py

# Step 4: Generate candidate generation jobs
conda run -n baer-refqa python scripts/generate_candidates.py

# Step 5: Generate simulated model predictions (for pilot)
conda run -n baer-refqa python scripts/generate_simulated_predictions.py

# Step 6: Run audit and tiering
conda run -n baer-refqa python scripts/run_audit.py
conda run -n baer-refqa python scripts/curate_tiers.py

# Step 7: Render report
conda run -n baer-refqa python scripts/render_report.py
```

Or run all at once:

```bash
conda run -n baer-refqa python scripts/run_pipeline.py
```

### 3. View Report

```bash
cat reports/pilot_audit_report.md
```

## Architecture

```
raw QA data → Semantic Families → Reference Bank
    → Generation Jobs → Audio Synthesis (CosyVoice / mock)
    → ASR (Whisper) → Validity Gates (Lexical + Prosodic)
    → Model Evaluation (C1–C5) → Audit Metrics
    → Gold/Silver/Bronze Tiering → Report
```

## Audit Conditions

| Condition | Description |
|---|---|
| C1 Text-Oracle | Perfect transcript, text model |
| C2 Text-ASR | ASR transcript, text model |
| C3 Speech-Natural | Natural speech, speech model |
| C4 Speech-Lexicalized | Flat prosody speech, speech model |
| C5 Speech-Revoiced | Re-voiced by different speaker |

## Audit Metrics

- **ASR Loss** = C1 - C2 (ASR degradation)
- **Modality Penalty** = C1 - C3 (speech vs text)
- **Incremental Audio Value** = C3 - C1 (audio contribution)
- **Prosody Sensitivity** = C3 - C4 (prosody importance)

## Sample Tiers

| Tier | Description |
|---|---|
| Gold | All gates pass + conclusive audit |
| Silver | Automatic gates pass, behavioral incomplete |
| Bronze | Plausible candidates for future iteration |
| Reject | Lexical failure, prompt leak, unusable |

## Project Status

- ✅ Repo scaffold + canonical schema
- ✅ Semantic family builder
- ✅ Reference bank index
- ✅ Generation planner (CosyVoice adapter)
- ✅ Validity gates (lexical + prosodic)
- ✅ Audit metric engine
- ✅ Gold/Silver/Bronze tiering
- ✅ Pilot data generator (300 synthetic samples)
- ✅ Model prediction simulator
- ✅ End-to-end pipeline
- 🔄 Pilot evaluation running

## License

MIT
