# backend/app/main.py
from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware
from .routers import specs

app = FastAPI(
    title="API Copilot — Spec Generator",
    description="Generate structured API specs + DB schema from messy requirements",
    version="1.0"
)

# CORS - allow any origin (safe since frontend is separate)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your specs router
app.include_router(specs.router, prefix="/specs")

# Beautiful root page — just like Socrates
@app.get("/", response_class=responses.HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>API Copilot — Spec Generator</title>
            <style>
                body { 
                    font-family: system-ui, -apple-system, sans-serif; 
                    margin: 40px auto; 
                    max-width: 800px; 
                    padding: 20px; 
                    background: #0f172a; 
                    color: #e2e8f0; 
                    line-height: 1.7; 
                }
                a { color: #38bdf8; text-decoration: none; }
                a:hover { text-decoration: underline; }
                h1 { color: #7dd3fc; }
                pre { background: #1e293b; padding: 12px; border-radius: 8px; color: #a5f3fc; }
                hr { border-color: #334155; }
                small { color: #94a3b8; }
            </style>
        </head>
        <body>
            <h1>API Copilot is Running</h1>
            <p>Backend is healthy and ready to generate clean specs from messy requirements.</p>
            <ul>
                <li>Interactive API documentation: <a href="/docs" target="_blank">Swagger UI (/docs)</a></li>
                <li>Alternative docs: <a href="/redoc" target="_blank">ReDoc (/redoc)</a></li>
                <li>Generate specs: <code>POST /specs/generate</code></li>
                <li>Refine specs: <code>POST /specs/refine</code></li>
            </ul>
            <p><strong>Frontend</strong> is hosted separately on Vercel and connects to this API.</p>
            <hr>
            <small>Deployed on Hugging Face Spaces • Powered by Groq + Llama 3.3</small>
        </body>
    </html>
    """

# Optional: Health endpoint
@app.get("/health")
def health():
    return {"status": "ok", "service": "API Copilot"}

# Startup logging — matches Socrates style
@app.on_event("startup")
async def startup_event():
    print("\n" + "="*70)
    print("API COPILOT — SPEC GENERATOR STARTED SUCCESSFULLY!")
    print("="*70)
    print("• CORS enabled (all origins)")
    print("• Router mounted: /specs/*")
    print("• Swagger UI available at /docs")
    print("• Versioning logs saved in backend/app/logs/")
    print("="*70 + "\n")
