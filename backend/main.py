from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import upload, jobs, download

app = FastAPI(title="VideoLingo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, tags=["upload"])
app.include_router(jobs.router, tags=["jobs"])
app.include_router(download.router, tags=["download"])


@app.get("/health")
def health():
    return {"status": "ok"}