from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.websocket_routes import router as websocket_router

app = FastAPI(title="Meeting Summarization API", version="1.0")

# Include routes
app.include_router(websocket_router)

# Serve static files
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run("app.main:app", host="0.0.0.0", port=8009, reload=True)
