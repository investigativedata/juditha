from enum import StrEnum
from typing import Set

from ftmq.enums import Schemata as _Schemata


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

    @classmethod
    def resolve(cls, schemata: Set[str]) -> str | None:
        if not schemata or not schemata & cls.schemata:
            return None
        for schema in schemata:
            if schema != Schemata.LegalEntity:
                return schema
        if Schemata.LegalEntity in schemata:
            return Schemata.LegalEntity
