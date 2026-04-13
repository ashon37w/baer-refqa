from pydantic import BaseModel

class GenerationJob(BaseModel):
    job_id: str
    family_id: str
    reference_id: str
    generation_mode: str
    transcript: str
    output_path: str
