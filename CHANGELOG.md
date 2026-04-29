# Changelog

## 0.3.0 (2026-04-28)

- Add `Schema.list_field(name, *, sep=",", item_type=str)` for parsing comma-separated list values with optional per-item type coercion (`str`, `int`, `float`)
- Add module docstring and `from __future__ import annotations` to package modules
- Fix `pyproject.toml` description to end with a period (matches README)

## 0.2.1 (2026-03-31)

- Standardize README to 3-badge format with emoji Support section
- Update CI checkout action to v5 for Node.js 24 compatibility

## 0.2.0 (2026-03-27)

- Add `Schema.generate_help()` method for formatted schema documentation
- Add `Schema.load_from_env_file(path)` method for .env file loading and validation
- Add 8 badges, Support section, and compliance fixes to README
- Add `[tool.pytest.ini_options]` and `[tool.mypy]` to pyproject.toml
- Add `.github/` issue templates, PR template, and Dependabot config

## 0.1.5

- Add Development section to README
- Add wheel build target to pyproject.toml

## 0.1.1

- Add project URLs to pyproject.toml

## 0.1.0
- Initial release
