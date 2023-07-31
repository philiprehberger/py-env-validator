# philiprehberger-env-validator

[![Tests](https://github.com/philiprehberger/py-env-validator/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-env-validator/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-env-validator.svg)](https://pypi.org/project/philiprehberger-env-validator/)
[![License](https://img.shields.io/github/license/philiprehberger/py-env-validator)](LICENSE)
[![Sponsor](https://img.shields.io/badge/sponsor-GitHub%20Sponsors-ec6cb9)](https://github.com/sponsors/philiprehberger)

Schema-based environment variable validation with type coercion and helpful error messages.

## Installation

```bash
pip install philiprehberger-env-validator
```

## Usage

### Basic Validation

```python
from philiprehberger_env_validator import Schema, validate

schema = (
    Schema()
    .string("DATABASE_URL", description="PostgreSQL connection string")
    .integer("PORT", default=3000)
    .boolean("DEBUG", default=False)
    .string("NODE_ENV", choices=["development", "staging", "production"])
)

config = validate(schema)
print(config["PORT"])  # 3000 (int, not string)
```

### Field Types

```python
schema = (
    Schema()
    .string("API_KEY")
    .integer("MAX_CONNECTIONS")
    .float_field("RATE_LIMIT")
    .boolean("VERBOSE")
    .url("WEBHOOK_URL")
    .email("ADMIN_EMAIL")
)
```

### Custom Validation

```python
schema = Schema().string(
    "API_KEY",
    pattern=r"^sk-[a-zA-Z0-9]{32}$",
    validator=lambda v: len(v) > 10,
)
```

### Optional Fields

```python
schema = (
    Schema()
    .string("REQUIRED_VAR")
    .string("OPTIONAL_VAR", required=False, default="fallback")
)
```

### Custom Source

```python
config = validate(schema, source={"PORT": "8080", "DEBUG": "true"})
```

### Error Handling

```python
from philiprehberger_env_validator import ValidationError

try:
    config = validate(schema)
except ValidationError as e:
    for error in e.errors:
        print(error)
```


## API

| Function / Class | Description |
|------------------|-------------|
| `validate(schema, source)` | Validate environment variables against a schema, returning typed dict |
| `Schema` | Fluent schema builder with `string()`, `integer()`, `float_field()`, `boolean()`, `url()`, `email()` methods |
| `FieldSpec` | Field specification with type, default, choices, pattern, and validator options |
| `ValidationError` | Raised when validation fails, contains list of error messages in `errors` |

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## License

MIT
