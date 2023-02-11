# hera-limit

---

## Table of Contents

- [License](#license)

hera limit is a rate limiter service. It allows defining rules as files and
limiting access to a path based on the rules.

## How To Use

### Define Rate Limiting Rules

The rules can be defined in YAML format:

```yaml
path: auth/* # apply to all requests going to auth/*
rules:
  - key: username # rate limit for each user based on username
    value: <optional> # apply rule to only requests that have this value as the key
    rate_limit:
      unit: <second, minute, hour> # the period which the rate limit resets
      request_per_unit: <number> # number of allowed reuqests
```

### Run the service

Run the service and pass the rules directory:

```bash
make run ./rules_dir
```

## License

`hera-limit` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
