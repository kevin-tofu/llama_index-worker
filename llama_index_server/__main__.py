
from dotenv import load_dotenv
load_dotenv('.env')
import os
import argparse
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from llama_index_server.routes import get_router
from llama_index_server.config import Config, RedisConfig
from llama_index_server.logconf import mylogger
logger = mylogger(__name__)


def get_server(cfg: Config):
    server = FastAPI()
    # app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    origins = ["*"]
    server.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        # allow_credentials=False,
        allow_methods=["*"],
        # allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    serverinfo = {
        "version": cfg.app_version
    }

    @server.get("/")
    def root():
        return serverinfo

    server.include_router(
        get_router(cfg)
    )
    return server


if __name__ == '__main__':


    APP_VERSION = os.getenv('APP_VERSION', 'v0.0.1')
    APP_PORT = int(os.getenv('APP_PORT', 80))
    LLM_NAME = os.getenv('LLM_NAME', '')
    LLM_KEY = os.getenv('LLM_NAME', '')
    EMBED_NAME = os.getenv('EMBED_NAME', '')
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))

    parser = argparse.ArgumentParser()
    parser.add_argument('--app_version', '-AV', type=str, default=APP_VERSION, help='')
    parser.add_argument('--app_port', '-AP', type=int, default=APP_PORT, help='port for http server')
    parser.add_argument('--llm_name', '-LM', type=str, default=LLM_NAME, help='')
    parser.add_argument('--llm_key', '-LK', type=str, default=LLM_KEY, help='')
    parser.add_argument('--embed_name', '-EN', type=str, default=EMBED_NAME, help='')
    parser.add_argument('--redis_host', '-RH', type=str, default=REDIS_HOST, help='')
    parser.add_argument('--redis_port', '-RP', type=int, default=REDIS_PORT, help='')
    args = parser.parse_args()

    cfg = Config.from_defaults(
        args.app_version,
        args.llm_name,
        args.llm_key,
        args.embed_name,
        args.redis_host,
        args.redis_port
    )
    print(cfg)

    server = get_server(cfg)

    uvicorn.run(
        server,
        host="0.0.0.0",
        port=args.app_port
    )