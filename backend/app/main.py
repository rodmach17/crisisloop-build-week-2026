from fastapi import FastAPI

app = FastAPI(
    title="CrisisLoop API",
    version="0.1.0",
    description="Backend for the CrisisLoop adaptive clinical crisis simulator.",
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "CrisisLoop API",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
    }
