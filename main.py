import asyncio
import os

from fastapi import FastAPI
from uvicorn import Config, Server
from starlette.middleware.cors import CORSMiddleware

from src.api.handler.error_handler import add_error_handler
from src.api.v1.router_v1 import router_v1

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_v1, prefix='/api')

add_error_handler(app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8008"))
    config = Config(app=app, host="0.0.0.0", port=port, log_level="info")
    server = Server(config)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(server.serve())
