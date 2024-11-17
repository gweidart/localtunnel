# LocalTunnel Python Client

[![PyPI version](https://badge.fury.io/py/localtunnel.svg)](https://pypi.org/project/localtunnel/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/localtunnel.svg)](https://pypi.org/project/localtunnel/)

Python port of the Localtunnel Client

Expose your localhost to the 🌎 for easy testing and sharing:

- 👷🏻‍♂️ Actively maintained

A Python client for [LocalTunnel](https://localtunnel.github.io/www/), enabling developers to expose their local servers to the internet with minimal setup. Designed for ease of use, flexibility, and lightweight integration, this library supports both CLI and programmatic APIs.

---

## Overview

LocalTunnel provides a simple way to make a local development server accessible to anyone on the internet. Unlike similar tools like Ngrok, this library is lightweight, open-source, and Python-native, making it perfect for developers who prefer seamless integration into their Python projects.

---

## Installation

Install using a package manager 📦:

### via `pip`

```bash
pip install localtunnel
```

### via `uv`

```bash
uv add localtunnel
```

### via `poetry`

```bash
poetry add Localtunnel
```

For contributors or advanced users, clone the repository and install in editable mode:

```bash
git clone https://github.com/gweidart/localtunnel.git
cd localtunnel
pip install -e .
```

---

## Features

- **Expose Local Servers Effortlessly**:

  - Quickly share your local development server with a public URL.
  - Perfect for testing webhooks, sharing progress with team members, or debugging remotely.

- **Custom Subdomains**:

  - Use a custom subdomain to make your server URL more predictable and user-friendly.
  - Example: `https://my-custom-subdomain.loca.lt`

- **Robust Retry Mechanisms**:

  - Ensure tunnel connections are resilient with customizable retry strategies, including exponential backoff.

- **Monitoring and Lifecycle Management**:

  - Built-in support for monitoring tunnels to handle unexpected disruptions.
  - Automatically recover or notify when a tunnel goes offline.

- **Flexible Header Transformations**:

  - Modify request headers dynamically using `HeaderTransformer`.

- **Lightweight CLI Tool**:

  - A simple command-line interface for quick setup and deployment.

- **Seamless Integration**:

  - Import the library directly into your Python project and manage tunnels programmatically.

- **Extensive Logging**:
  - Fully customizable logging via [Loguru](https://loguru.readthedocs.io/).

---

## Quick Start

### Programmatic API

Here’s how to expose a local server programmatically:

```python
import asyncio
from localtunnel.tunnel_manager import TunnelManager

async def main():
    manager = TunnelManager()
    manager.add_tunnel(port=8000, subdomain="my-subdomain")

    try:
        await manager.open_all()
        for tunnel in manager.tunnels:
            print(f"Tunnel open at URL: {tunnel.get_tunnel_url()}")

        # Keep running
        await asyncio.Event().wait()
    finally:
        await manager.close_all()

asyncio.run(main())
```

---

### CLI Usage

Expose a local server directly from the command line:

```bash
lt --port 3002 -s my-subdomain
```

Available arguments:

| Argument          | Description                                                                |
| ----------------- | -------------------------------------------------------------------------- |
| `-p, --port`      | Local port to expose via the tunnel (required).                            |
| `-s, --subdomain` | Optional subdomain for the tunnel.                                         |
| `-t, --host`      | LocalTunnel server URL (default: `https://localtunnel.me`).                |
| `-m, --monitor`   | Enable monitoring of the tunnel.                                           |
| `-l, --log-level` | Set the log level (e.g., `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). |

---

## Advanced Usage

### Create a new localtunnel

```python
import asyncio
from localtunnel.tunnel_manager import TunnelManager

async def main():
    manager = TunnelManager()
    manager.add_tunnel(port=8000, subdomain="my-subdomain")

    try:
        await manager.open_all()
        for tunnel in manager.tunnels:
            print(f"Tunnel open at URL: {tunnel.get_tunnel_url()}")

        # Keep running
        await asyncio.Event().wait()
    finally:
        await manager.close_all()

asyncio.run(main())

```

```

```

### Custom Header Transformations

Modify headers dynamically using `HeaderTransformer`:

```python
from localtunnel.header_transformer import HeaderTransformerFactory

transformer = HeaderTransformerFactory.create_transformer(
    transformer_type="host", host="my-custom-host"
)
headers = {"Authorization": "Bearer token"}
transformed_headers = transformer.transform(headers)
print(transformed_headers)
```

---

### Retry Strategies

Implement robust retry mechanisms for tunnel connections:

```python
from localtunnel.utils import ExponentialBackoffRetryTemplate

retry_strategy = ExponentialBackoffRetryTemplate(base_delay=1.0, max_delay=10.0)
retry_strategy.retry(some_function, retries=5)
```

---

### Managing Multiple Tunnels

Use `TunnelManager` to handle multiple tunnels seamlessly:

```python
from localtunnel.tunnel_manager import TunnelManager

manager = TunnelManager()
manager.add_tunnel(port=8000, subdomain="app1")
manager.add_tunnel(port=8001, subdomain="app2")
await manager.open_all()
```

---

## Troubleshooting

- **Issue**: Tunnel connection drops frequently.

  - **Solution**: Enable monitoring with `TunnelManager`.

- **Issue**: Logs are too verbose.

  - **Solution**: Customize log levels using `--log-level` in the CLI or `logger.add()` in code.

- **Issue**: Custom subdomain not working.
  - **Solution**: Ensure the subdomain is available and correctly passed to `add_tunnel()`.

---

## Contributing

We welcome contributions! Here's how you can get involved:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Links and Acknowledgments

- [Source Code](https://github.com/gweidart/localtunnel)
- [Issue Tracker](https://github.com/gweidart/localtunnel/issues)
- [Documentation](https://github.com/gweidart/localtunnel#readme)
