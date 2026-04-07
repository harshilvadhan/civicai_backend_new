from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import complaints, officer, upload

app = FastAPI(
    title="CivicAI Backend API",
    description="Backend for the AI-powered Civic Complaint Routing System",
    version="1.0.0"
)

# ─── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(complaints.router, prefix="/complaints", tags=["Complaints"])
app.include_router(officer.router,    prefix="/officer",    tags=["Officer"])
app.include_router(upload.router,     prefix="/upload",     tags=["Upload"])

@app.get("/", tags=["Health"])
def health():
    return {"status": "CivicAI backend is live ✅"}
