from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Any, Callable


class ValidationError(Exception):
    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        msg = f"{len(errors)} validation error(s):\n" + "\n".join(f"  - {e}" for e in errors)
        super().__init__(msg)


@dataclass
class FieldSpec:
    required: bool = True
    type: str = "str"
    default: Any = None
    choices: list[str] | None = None
    pattern: str | None = None
    validator: Callable[[str], bool] | None = None
    description: str = ""


@dataclass
class Schema:
    fields: dict[str, FieldSpec] = field(default_factory=dict)

    def string(self, name: str, **kwargs: Any) -> Schema:
        self.fields[name] = FieldSpec(type="str", **kwargs)
        return self

    def integer(self, name: str, **kwargs: Any) -> Schema:
        self.fields[name] = FieldSpec(type="int", **kwargs)
        return self

    def float_field(self, name: str, **kwargs: Any) -> Schema:
        self.fields[name] = FieldSpec(type="float", **kwargs)
        return self

    def boolean(self, name: str, **kwargs: Any) -> Schema:
        self.fields[name] = FieldSpec(type="bool", **kwargs)
        return self

    def url(self, name: str, **kwargs: Any) -> Schema:
        self.fields[name] = FieldSpec(type="url", **kwargs)
        return self

    def email(self, name: str, **kwargs: Any) -> Schema:
        self.fields[name] = FieldSpec(type="email", **kwargs)
        return self


def _coerce(value: str, type_name: str) -> Any:
    if type_name == "str":
        return value
    if type_name == "int":
        return int(value)
    if type_name == "float":
        return float(value)
    if type_name == "bool":
        return value.lower() in ("true", "1", "yes", "on")
    if type_name == "url":
        return value
    if type_name == "email":
        return value
    return value


_URL_RE = re.compile(r"^https?://\S+$")
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate(
    schema: Schema,
    source: dict[str, str] | None = None,
) -> dict[str, Any]:
    env = source if source is not None else dict(os.environ)
    errors: list[str] = []
    result: dict[str, Any] = {}

    for name, spec in schema.fields.items():
        raw = env.get(name)

        if raw is None or raw == "":
            if spec.default is not None:
                result[name] = spec.default
                continue
            if spec.required:
                desc = f" ({spec.description})" if spec.description else ""
                errors.append(f"Missing required variable: {name}{desc}")
            continue

        if spec.choices and raw not in spec.choices:
            errors.append(f"{name} must be one of {spec.choices}, got '{raw}'")
            continue

        if spec.pattern and not re.match(spec.pattern, raw):
            errors.append(f"{name} does not match pattern '{spec.pattern}'")
            continue

        if spec.type == "url" and not _URL_RE.match(raw):
            errors.append(f"{name} is not a valid URL")
            continue

        if spec.type == "email" and not _EMAIL_RE.match(raw):
            errors.append(f"{name} is not a valid email address")
            continue

        try:
            coerced = _coerce(raw, spec.type)
        except (ValueError, TypeError):
            errors.append(f"{name} cannot be converted to {spec.type}: '{raw}'")
            continue

        if spec.validator and not spec.validator(raw):
            errors.append(f"{name} failed custom validation")
            continue

        result[name] = coerced

    if errors:
        raise ValidationError(errors)

    return result
