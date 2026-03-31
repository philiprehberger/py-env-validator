# philiprehberger-env-validator

[![Tests](https://github.com/philiprehberger/py-env-validator/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-env-validator/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-env-validator.svg)](https://pypi.org/project/philiprehberger-env-validator/)
[![Last updated](https://img.shields.io/github/last-commit/philiprehberger/py-env-validator)](https://github.com/philiprehberger/py-env-validator/commits/main)

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

### Schema Documentation

Generate formatted help text documenting all fields, grouped by required and optional.

```python
schema = (
    Schema()
    .url("DATABASE_URL", description="PostgreSQL connection string")
    .string("API_KEY")
    .boolean("DEBUG", default=False, required=False, description="Enable debug mode")
    .integer("PORT", default=8000, required=False)
)

print(schema.generate_help())
# REQUIRED:
#   DATABASE_URL (url): PostgreSQL connection string
#   API_KEY (str): No description
#
# OPTIONAL:
#   DEBUG (bool) [default: false]: Enable debug mode
#   PORT (int) [default: 8000]: No description
```

### Load from .env File

Read and validate a `.env` file directly against a schema.

```python
schema = (
    Schema()
    .string("DATABASE_URL")
    .integer("PORT", default=3000)
    .boolean("DEBUG", default=False)
)

config = schema.load_from_env_file(".env")
print(config["DATABASE_URL"])
print(config["PORT"])  # coerced to int
```

The `.env` file uses standard `KEY=VALUE` format. Comments (`#`) and blank lines are skipped. Quoted values are unquoted automatically.

## API

| Function / Class | Description |
|---|---|
| `validate(schema, source)` | Validate environment variables against a schema, returning typed dict |
| `Schema` | Fluent schema builder with `string()`, `integer()`, `float_field()`, `boolean()`, `url()`, `email()` methods |
| `Schema.generate_help()` | Return formatted help text documenting all fields grouped by required/optional |
| `Schema.load_from_env_file(path)` | Load and validate a `.env` file against the schema |
| `FieldSpec` | Field specification with type, default, choices, pattern, validator, and description options |
| `ValidationError` | Raised when validation fails, contains list of error messages in `errors` |

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## Support

If you find this project useful:

⭐ [Star the repo](https://github.com/philiprehberger/py-env-validator)

🐛 [Report issues](https://github.com/philiprehberger/py-env-validator/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

💡 [Suggest features](https://github.com/philiprehberger/py-env-validator/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)

❤️ [Sponsor development](https://github.com/sponsors/philiprehberger)

🌐 [All Open Source Projects](https://philiprehberger.com/open-source-packages)

💻 [GitHub Profile](https://github.com/philiprehberger)

🔗 [LinkedIn Profile](https://www.linkedin.com/in/philiprehberger)

## License

[MIT](LICENSE)
