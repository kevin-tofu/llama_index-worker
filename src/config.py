import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class Config():
    model: str
    model_name: str
    model_key: Optional[str]


    @classmethod
    def from_defaults(
        cls,
        model: str,
        model_name: str,
        model_key: str
    ) -> 'Config':
        
        return cls(
            model,
            model_name,
            model_key
        )