from app.api.v1.endpoints import auth, analysis, reports, users

api_router = auth.router
api_router.include_router(analysis.router)
api_router.include_router(reports.router)
api_router.include_router(users.router)
