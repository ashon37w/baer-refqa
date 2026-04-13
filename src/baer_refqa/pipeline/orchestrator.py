"""End-to-end BAER/REF-QA pipeline orchestrator."""
import json
import logging
from pathlib import Path
from dataclasses import dataclass

from baer_refqa.settings import Settings
from baer_refqa.text.family_builder import build_semantic_family
from baer_refqa.reference_bank.index import rank_references
from baer_refqa.reference_bank.models import ReferenceClip, ReferenceQuery
from baer_refqa.generation.planner import build_generation_jobs
from baer_refqa.generation.cosyvoice_adapter import CosyVoiceAdapter
from baer_refqa.curation.tiering import decide_tier
from baer_refqa.schema import SampleRecord, GateResult

logger = logging.getLogger(__name__)


@dataclass
class BAERPipeline:
    settings: Settings
    use_mock_synthesis: bool = True

    def run_full(self) -> Path:
        self.settings.ensure_dirs()
        self._synthesize()
        self._tier()
        return self.settings.artifact_dir / "audit" / "tiered_samples.jsonl"

    @staticmethod
    def list_stages() -> list[str]:
        return ["synthesis", "asr", "audit", "tiering"]

    def _synthesize(self) -> None:
        logger.info("Stage: Synthesis")
        adapter = CosyVoiceAdapter(use_mock=self.use_mock_synthesis)
        manifest_path = self.settings.artifact_dir / "generation" / "generation_jobs.jsonl"
        if not manifest_path.exists():
            logger.warning(f"Manifest not found: {manifest_path} — skipping synthesis")
            return
        for line in open(manifest_path, encoding="utf-8"):
            if not line.strip():
                continue
            job_dict = json.loads(line)
            # Convert dict to object with dot access
            job = type("Job", (), job_dict)()
            adapter.run_job(type("Job", (), job_dict)())
        logger.info("Synthesis complete")

    def _tier(self) -> None:
        logger.info("Stage: Tiering")
        enriched = self.settings.artifact_dir / "audit" / "enriched_samples.jsonl"
        tiered = self.settings.artifact_dir / "audit" / "tiered_samples.jsonl"
        if not enriched.exists():
            logger.warning(f"Enriched samples not found: {enriched} — skipping tiering")
            return
        tiered.parent.mkdir(parents=True, exist_ok=True)
        with enriched.open(encoding="utf-8") as fin, tiered.open("w", encoding="utf-8") as fout:
            for line in fin:
                if not line.strip():
                    continue
                sample = SampleRecord.model_validate_json(line)
                sample.tier = decide_tier(sample)
                fout.write(json.dumps(sample.model_dump(), ensure_ascii=False) + "\n")
        logger.info(f"Tiering complete → {tiered}")
