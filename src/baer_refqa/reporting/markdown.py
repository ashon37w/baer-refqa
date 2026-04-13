def render_report(project_name: str, slice_rows: list[dict], risks: list[str]) -> str:
    lines = [
        f"# {project_name} Audit Report",
        "",
        "## Slice Summary",
        "",
        "| slice | n | ASR Loss | Modality Penalty | Incremental Audio Value | Prosody Sensitivity | label |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in slice_rows:
        lines.append(
            f"| {row['task_slice']} | {row['n']} | {row['asr_loss']:.3f} | {row['modality_penalty']:.3f} | {row['incremental_audio_value']:.3f} | {row['prosody_sensitivity']:.3f} | {row['label']} |"
        )
    lines.extend(["", "## Risks", ""])
    for risk in risks:
        lines.append(f"- {risk}")
    return "\n".join(lines)
