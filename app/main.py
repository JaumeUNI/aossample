from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from app.routes import sample

app = FastAPI()

# Configure CORS to allow requests from the web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the project root directory
project_root = Path(__file__).parent.parent

# Include the sample routes FIRST (so API routes take precedence)
app.include_router(sample.router)

# Serve index.html at root
@app.get("/", include_in_schema=False)
async def read_root():
    index_path = project_root / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "API is running. Visit /docs for documentation."}

# Serve specific static files
@app.get("/styles.css", include_in_schema=False)
async def serve_css():
    css_path = project_root / "styles.css"
    if css_path.exists():
        return FileResponse(str(css_path), media_type="text/css")
    from fastapi import HTTPException
    raise HTTPException(status_code=404)

@app.get("/app.js", include_in_schema=False)
async def serve_js():
    js_path = project_root / "app.js"
    if js_path.exists():
        return FileResponse(str(js_path), media_type="application/javascript")
    from fastapi import HTTPException
    raise HTTPException(status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
