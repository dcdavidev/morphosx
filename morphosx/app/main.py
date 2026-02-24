from fastapi import FastAPI
from morphosx.app.api.assets import router as assets_router
from morphosx.app.settings import settings

def create_app() -> FastAPI:
    """
    Initialize and configure the FastAPI application.
    
    :return: FastAPI instance.
    """
    app = FastAPI(
        title=settings.app_name,
        description="High-performance OSS cloud storage for on-the-fly image processing.",
        version="0.1.0"
    )

    # Register API routes
    app.include_router(assets_router, prefix=settings.api_prefix)

    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint to verify service status."""
        return {"status": "ok", "app": settings.app_name}

    return app

# Main entry point for uvicorn
app = create_app()
