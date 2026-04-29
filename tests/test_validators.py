from __future__ import annotations

import pytest

from philiprehberger_env_validator import FieldSpec, Schema, ValidationError, validate


def test_validate_required_string() -> None:
    schema = Schema().string("APP_NAME")
    result = validate(schema, source={"APP_NAME": "myapp"})
    assert result == {"APP_NAME": "myapp"}


def test_validate_missing_required_raises() -> None:
    schema = Schema().string("APP_NAME")
    with pytest.raises(ValidationError) as exc_info:
        validate(schema, source={})
    assert "Missing required variable: APP_NAME" in exc_info.value.errors


def test_validate_optional_with_default() -> None:
    schema = Schema().string("PORT", required=False, default="3000")
    result = validate(schema, source={})
    assert result == {"PORT": "3000"}


def test_validate_integer_coercion() -> None:
    schema = Schema().integer("PORT")
    result = validate(schema, source={"PORT": "8080"})
    assert result == {"PORT": 8080}


def test_validate_integer_invalid_raises() -> None:
    schema = Schema().integer("PORT")
    with pytest.raises(ValidationError) as exc_info:
        validate(schema, source={"PORT": "abc"})
    assert "cannot be converted to int" in exc_info.value.errors[0]


def test_validate_float_coercion() -> None:
    schema = Schema().float_field("RATE")
    result = validate(schema, source={"RATE": "3.14"})
    assert result == {"RATE": 3.14}


def test_validate_boolean_true_values() -> None:
    schema = Schema().boolean("DEBUG")
    for val in ("true", "1", "yes", "on"):
        result = validate(schema, source={"DEBUG": val})
        assert result["DEBUG"] is True


def test_validate_boolean_false_values() -> None:
    schema = Schema().boolean("DEBUG")
    for val in ("false", "0", "no", "off"):
        result = validate(schema, source={"DEBUG": val})
        assert result["DEBUG"] is False


def test_validate_choices() -> None:
    schema = Schema().string("ENV", choices=["dev", "staging", "prod"])
    result = validate(schema, source={"ENV": "prod"})
    assert result == {"ENV": "prod"}


def test_validate_choices_invalid_raises() -> None:
    schema = Schema().string("ENV", choices=["dev", "staging", "prod"])
    with pytest.raises(ValidationError) as exc_info:
        validate(schema, source={"ENV": "test"})
    assert "must be one of" in exc_info.value.errors[0]


def test_validate_pattern() -> None:
    schema = Schema().string("API_KEY", pattern=r"^sk-[a-z0-9]+$")
    result = validate(schema, source={"API_KEY": "sk-abc123"})
    assert result == {"API_KEY": "sk-abc123"}


def test_validate_pattern_invalid_raises() -> None:
    schema = Schema().string("API_KEY", pattern=r"^sk-[a-z0-9]+$")
    with pytest.raises(ValidationError) as exc_info:
        validate(schema, source={"API_KEY": "bad-key"})
    assert "does not match pattern" in exc_info.value.errors[0]


def test_validate_url_valid() -> None:
    schema = Schema().url("HOMEPAGE")
    result = validate(schema, source={"HOMEPAGE": "https://example.com"})
    assert result == {"HOMEPAGE": "https://example.com"}


def test_validate_url_invalid_raises() -> None:
    schema = Schema().url("HOMEPAGE")
    with pytest.raises(ValidationError) as exc_info:
        validate(schema, source={"HOMEPAGE": "not-a-url"})
    assert "not a valid URL" in exc_info.value.errors[0]


def test_validate_email_valid() -> None:
    schema = Schema().email("CONTACT")
    result = validate(schema, source={"CONTACT": "user@example.com"})
    assert result == {"CONTACT": "user@example.com"}


def test_validate_email_invalid_raises() -> None:
    schema = Schema().email("CONTACT")
    with pytest.raises(ValidationError) as exc_info:
        validate(schema, source={"CONTACT": "not-email"})
    assert "not a valid email" in exc_info.value.errors[0]


def test_validate_custom_validator() -> None:
    schema = Schema().string("PORT", validator=lambda v: v.isdigit())
    result = validate(schema, source={"PORT": "8080"})
    assert result == {"PORT": "8080"}


def test_validate_custom_validator_fails() -> None:
    schema = Schema().string("PORT", validator=lambda v: v.isdigit())
    with pytest.raises(ValidationError) as exc_info:
        validate(schema, source={"PORT": "abc"})
    assert "failed custom validation" in exc_info.value.errors[0]


def test_validate_multiple_errors() -> None:
    schema = Schema().string("A").string("B").integer("C")
    with pytest.raises(ValidationError) as exc_info:
        validate(schema, source={})
    assert len(exc_info.value.errors) == 3


def test_validate_description_in_error() -> None:
    schema = Schema().string("SECRET", description="API secret key")
    with pytest.raises(ValidationError) as exc_info:
        validate(schema, source={})
    assert "API secret key" in exc_info.value.errors[0]


def test_validation_error_message() -> None:
    schema = Schema().string("A").string("B")
    with pytest.raises(ValidationError) as exc_info:
        validate(schema, source={})
    assert "2 validation error(s)" in str(exc_info.value)


def test_schema_chaining() -> None:
    schema = Schema().string("A").integer("B").boolean("C")
    assert len(schema.fields) == 3
    assert schema.fields["A"].type == "str"
    assert schema.fields["B"].type == "int"
    assert schema.fields["C"].type == "bool"


def test_empty_string_treated_as_missing() -> None:
    schema = Schema().string("APP_NAME")
    with pytest.raises(ValidationError):
        validate(schema, source={"APP_NAME": ""})


def test_validate_list_default_str_items() -> None:
    schema = Schema().list_field("HOSTS")
    result = validate(schema, source={"HOSTS": "a.com,b.com,c.com"})
    assert result == {"HOSTS": ["a.com", "b.com", "c.com"]}


def test_validate_list_int_items() -> None:
    schema = Schema().list_field("PORTS", item_type=int)
    result = validate(schema, source={"PORTS": "80,443,8080"})
    assert result == {"PORTS": [80, 443, 8080]}


def test_validate_list_float_items() -> None:
    schema = Schema().list_field("WEIGHTS", item_type=float)
    result = validate(schema, source={"WEIGHTS": "1.0,2.5,3.7"})
    assert result == {"WEIGHTS": [1.0, 2.5, 3.7]}


def test_validate_list_custom_separator() -> None:
    schema = Schema().list_field("PATHS", sep=":")
    result = validate(schema, source={"PATHS": "/usr/bin:/usr/local/bin:/opt/bin"})
    assert result == {"PATHS": ["/usr/bin", "/usr/local/bin", "/opt/bin"]}


def test_validate_list_strips_whitespace_and_empty() -> None:
    schema = Schema().list_field("HOSTS")
    result = validate(schema, source={"HOSTS": "a.com, b.com ,, c.com"})
    assert result == {"HOSTS": ["a.com", "b.com", "c.com"]}


def test_validate_list_invalid_int_raises() -> None:
    schema = Schema().list_field("PORTS", item_type=int)
    with pytest.raises(ValidationError) as exc_info:
        validate(schema, source={"PORTS": "80,not-a-port"})
    assert "cannot be converted to list" in exc_info.value.errors[0]


def test_validate_list_optional_with_default() -> None:
    schema = Schema().list_field("TAGS", required=False, default=[])
    result = validate(schema, source={})
    assert result == {"TAGS": []}

