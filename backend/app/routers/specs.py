# backend/app/routers/specs.py
from fastapi import APIRouter, Request, HTTPException, status
from pydantic import BaseModel, Field, validator
from ..pipeline import run_pipeline, run_refinement
from ..utils.rate_limiter import limiter

router = APIRouter()

# === Generate new spec ===
class GenerateRequest(BaseModel):
    requirements_text: str = Field(
        ..., 
        min_length=50, 
        max_length=10000,
        description="Detailed product requirements (at least 50 characters to ensure meaningful output)"
    )

    @validator("requirements_text")
    def strip_and_check(cls, v):
        stripped = v.strip()
        if not stripped:
            raise ValueError("Requirements text cannot be empty or whitespace only")
        if len(stripped) < 50:
            raise ValueError(
                f"Requirements text is too short ({len(stripped)} characters). "
                "Please provide at least 50 characters with more detailed description of the product/features. "
                "Short inputs like 'build a todo app' produce poor results."
            )
        return stripped

@router.post("/generate")
async def generate_spec(request: Request, body: GenerateRequest):
    client_ip = request.client.host
    if not limiter.is_allowed(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    spec, trace_id = run_pipeline(body.requirements_text)
    if spec is None:
        raise HTTPException(status_code=500, detail=f"Generation failed. Trace: {trace_id}")
    return {"trace_id": trace_id, "spec": spec}

# === Refine existing spec ===
class RefineRequest(BaseModel):
    current_spec: dict
    refinement_text: str = Field(..., min_length=10, max_length=2000)
    trace_id: str  # Required: same trace_id from original generation

    @validator("refinement_text")
    def strip_and_check(cls, v):
        stripped = v.strip()
        if not stripped:
            raise ValueError("Refinement text cannot be empty")
        return stripped

@router.post("/refine")
async def refine_spec_endpoint(request: Request, body: RefineRequest):
    client_ip = request.client.host
    if not limiter.is_allowed(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    refined_spec, trace_id = run_refinement(
        current_spec=body.current_spec,
        refinement_text=body.refinement_text,
        base_trace_id=body.trace_id  # Pass the original trace_id
    )
    if refined_spec is None:
        raise HTTPException(status_code=500, detail=f"Refinement failed. Trace: {trace_id}")
    return {"trace_id": trace_id, "spec": refined_spec}