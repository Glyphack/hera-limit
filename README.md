# hera-limit

---

## Table of Contents

- [License](#license)

hera limit is a rate limiter service. It allows defining rules as files and
limiting access to a path based on the rules.

## How To Use

### Define Rate Limiting Rules

The rules can be defined in YAML format in a similar structure to
[envoy ratelimit](https://github.com/envoyproxy/ratelimit).

```json
{
  "path": "auth",
  "descriptors": [
    {
      "key": "auth_type",
      "value": "login",
      "rate_limit": {
        "unit": "minute",
        "requests_per_unit": 5
      }
    }
  ]
}
```

### Run the service

Run the service and pass the rules directory:

```bash
make run ./rules_dir
```

### Configuration

The following configuration are supported:

```json
{
  "cache_backend": "<local|redis>"
}
```

## License

`hera-limit` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
