from app.core.logger import logger
from app.factory import create_app, init_db

app = create_app()


@app.on_event("startup")
async def on_startup():
    await init_db()


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting uvicorn in reload mode")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=int("8000"),
    )