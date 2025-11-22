from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Include the sample routes
app.include_router(sample.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
