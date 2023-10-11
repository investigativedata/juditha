from enum import StrEnum
from typing import Generator, Set

from ftmq.enums import Schemata as _Schemata
from ftmq.types import CE

from juditha.util import canonized_names


class Schemata(StrEnum):
    """
    Actual schemata to classify for
    """

    LegalEntity = _Schemata.LegalEntity
    Person = _Schemata.Person
    Organization = _Schemata.Organization
    PublicBody = _Schemata.PublicBody
    Company = _Schemata.Company


class Schema:
    schemata = set(Schemata._member_names_)

    @staticmethod
    def to_ner_label(schema: Schemata) -> str:
        if schema == _Schemata.Person:
            return "PERSON"
        return "ORG"

    @staticmethod
    def from_proxy(proxy: CE) -> Generator[tuple[str, str], None, None]:
        schema = proxy.schema.name
        if schema in Schemata._member_names_:
            for name in canonized_names(proxy):
                yield name, schema

    @classmethod
    def resolve(cls, schemata: Set[str]) -> str | None:
        if not schemata or not schemata & cls.schemata:
            return None
        for schema in schemata:
            if schema != Schemata.LegalEntity:
                return schema
        if Schemata.LegalEntity in schemata:
            return Schemata.LegalEntity
