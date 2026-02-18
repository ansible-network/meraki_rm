# Meraki Dashboard Mock Server

A stateful Flask mock server that auto-generates routes from the Meraki OpenAPI spec (`spec3.json`), validates requests, and maintains in-memory CRUD state for integration testing.

## Quick Start

```bash
# From the collection root
python -m tools.mock_server --spec spec3.json --port 29443

# Health check
curl http://127.0.0.1:29443/health
```

## Architecture

```
spec3.json
    |
    v
spec_loader.py -----> Parses paths, extracts schemas, infers primary keys
    |
    v
server.py ----------> Registers Flask routes for every path in the spec
    |                  Routes delegate to state_store for CRUD
    v
state_store.py -----> In-memory dict-of-dicts
    |                  POST   -> create, 201
    |                  GET    -> retrieve/list, 200
    |                  PUT    -> update, 200
    |                  DELETE -> remove, 204
    v
response_generator.py -> Fills required fields with schema defaults
                          Merges state data with schema expectations
```

## Usage

### Standalone

```bash
python -m tools.mock_server --spec spec3.json --port 29443
```

### With Molecule

The `extensions/molecule/default/create.yml` playbook starts the mock server.
All module scenarios run against it via the shared inventory.

### State Management

```bash
# Reset all state
curl -X POST http://127.0.0.1:29443/_state/reset

# Dump current state (debugging)
curl http://127.0.0.1:29443/_state/dump
```

## Adapting for Another Spec

1. Replace `spec3.json` with the new OpenAPI spec
2. Adjust `spec_loader.infer_primary_key()` if the new API uses non-standard path parameters
3. Add custom behavior in `server.py` if needed (e.g., pagination, rate limiting)
4. The auto-routing, state store, and response generation work unchanged

## Dependencies

- `flask>=3.0.0`
- `openapi-core>=0.19.0` (for future request/response validation)
- `pyyaml>=6.0.0`
