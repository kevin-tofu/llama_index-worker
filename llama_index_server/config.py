import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class RedisConfig():
    redis_host: str
    redis_port: int

    @classmethod
    def from_defaults(
        cls,
        host: str,
        port: int
    ) -> 'RedisConfig':
        
        return cls(
            host,
            port
        )


@dataclass
class Config():
    app_version: str
    llm_name: str
    llm_key: Optional[str]
    embedmodel: str
    redis: RedisConfig


    @classmethod
    def from_defaults(
        cls,
        app_version: str,
        llm_name: str,
        llm_key: Optional[str],
        embed_name: str,
        redis_host: str,
        redis_port: int
    ) -> 'Config':
        
        redis = RedisConfig.from_defaults(redis_host, redis_port)
        return cls(
            app_version,
            llm_name,
            llm_key,
            embed_name,
            redis
        )