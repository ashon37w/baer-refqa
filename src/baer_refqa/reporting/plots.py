from pathlib import Path
import matplotlib.pyplot as plt

def plot_iav_vs_ps(rows: list[dict], output_path: Path) -> None:
    x = [row["incremental_audio_value"] for row in rows]
    y = [row["prosody_sensitivity"] for row in rows]
    labels = [row["task_slice"] for row in rows]
    plt.figure(figsize=(6, 4))
    plt.scatter(x, y)
    for idx, label in enumerate(labels):
        plt.annotate(label, (x[idx], y[idx]))
    plt.xlabel("Incremental Audio Value")
    plt.ylabel("Prosody Sensitivity")
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=160)
    plt.close()
