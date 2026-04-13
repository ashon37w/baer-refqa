import json
from pathlib import Path
from baer_refqa.reporting.markdown import render_report
from baer_refqa.reporting.plots import plot_iav_vs_ps

def main() -> None:
    source = Path("artifacts/audit/slice_summary.json")
    payload = json.loads(source.read_text(encoding="utf-8"))
    markdown = render_report(
        project_name=payload["project_name"],
        slice_rows=payload["slice_rows"],
        risks=payload["risks"],
    )
    report_path = Path("reports/pilot_audit_report.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(markdown, encoding="utf-8")
    plot_iav_vs_ps(payload["slice_rows"], Path("reports/pilot_iav_vs_ps.png"))
    print(report_path)

if __name__ == "__main__":
    main()
