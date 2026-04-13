# Architecture

1. Normalize raw QA rows into semantic families.
2. Rank Emilia references from metadata.
3. Expand each family into multi-candidate generation jobs.
4. Run lexical, prosodic, automatic-label, and behavioral gates.
5. Aggregate C1-C5 predictions into audit metrics.
6. Curate Gold / Silver / Bronze outputs and publish reports.
