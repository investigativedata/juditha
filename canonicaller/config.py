from functools import cache

from ftmq.model.mixins import YamlMixin
from pydantic import BaseModel

from canonicaller.settings import STORE_CONFIG
from canonicaller.source import Source


class Config(BaseModel, YamlMixin):
    sources = list[Source]


@cache
def get_config(uri: str | None = None) -> Config:
    uri = uri or STORE_CONFIG
    if uri:
        return Config.from_path(uri)
    return Config()
