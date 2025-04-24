from uuid import UUID
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from lib.logging import log
from providers.get_providers import get_provider, get_providers
from server.startup import lifespan


app = FastAPI(
    lifespan=lifespan,
)


@app.get("/providers")
def providers():
    return get_providers()


@app.get("/providers/{id}")
def provider(id: UUID):
    log(f"Fetching provider with ID: {id}")
    if provider := get_provider(id):
        return provider

    return JSONResponse(
        status_code=404,
        content={"message": "Provider not found"},
    )
