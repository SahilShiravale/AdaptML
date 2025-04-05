"""
Application initialization module.

This module initializes the FastAPI application with all necessary configurations,
middleware, exception handlers, and routers.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    app = FastAPI(
        title="AI Learning Recommendation API",
        description="API for AI-powered learning recommendations",
        version="1.0.0",
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Import and include routers
    from app.routes import auth, courses, recommendations
    
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
    app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])
    
    @app.get("/", tags=["Health Check"])
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "message": "API is running"}
    
    return app