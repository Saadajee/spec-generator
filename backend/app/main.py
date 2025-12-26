# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import specs

app = FastAPI(
    title="Spec Generator API",
    description="Generate structured specs from messy requirements",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CHANGE THIS LINE: remove prefix="/specs" or set to ""
app.include_router(specs.router, prefix="/specs")

@app.get("/")
async def root():
    return {"message": "API Copilot backend running"}