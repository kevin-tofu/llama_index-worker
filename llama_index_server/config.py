import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class ConfigRedis():
    redis_host: str
    redis_port: int

    @classmethod
    def from_defaults(
        cls,
        host: str,
        port: int
    ) -> 'ConfigRedis':
        
        return cls(
            host,
            port
        )


@dataclass
class Config():
    llm: str
    llm_name: str
    llm_key: Optional[str]
    embedmodel: str
    redis: ConfigRedis


    @classmethod
    def from_defaults(
        cls,
        llm: str,
        llm_name: str,
        llm_key: Optional[str],
        embedmodel: str,
        redis_host: str,
        redis_port: int
    ) -> 'Config':
        
        redis = ConfigRedis.from_defaults(redis_host, redis_port)
        return cls(
            llm,
            llm_name,
            llm_key,
            embedmodel,
            redis
        )