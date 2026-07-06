## Contents

- Installation
- Getting Started
- Configuration
- Async Python SDK




The Daytona Python SDK provides a robust interface for programmatically interacting with Daytona Sandboxes.

## Installation

Install the Daytona Python SDK using pip:

```bash
pip install daytona
```

Or using poetry:

```bash
poetry add daytona
```

## Getting Started

### Create a Sandbox

Create a Daytona Sandbox to run your code securely in an isolated environment. The following snippet is an example "Hello World" program that runs securely inside a Daytona Sandbox.

**Sync:**

```python
from daytona import Daytona

def main():
    # Initialize the SDK (uses environment variables by default)
    daytona = Daytona()

    # Create a new sandbox
    sandbox = daytona.create()

    # Execute a command
    response = sandbox.process.exec("echo 'Hello, World!'")
    print(response.result)

if __name__ == "__main__":
    main()
```

**Async:**

```python
import asyncio
from daytona import AsyncDaytona

async def main():
    # Initialize the SDK (uses environment variables by default)
    async with AsyncDaytona() as daytona:
        # Create a new sandbox
        sandbox = await daytona.create()

        # Execute a command
        response = await sandbox.process.exec("echo 'Hello, World!'")
        print(response.result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

The Daytona SDK can be configured using environment variables or by passing options to the constructor:

**Sync:**

```python
from daytona import Daytona, DaytonaConfig

# Using environment variables (DAYTONA_API_KEY, DAYTONA_API_URL, DAYTONA_TARGET)
daytona = Daytona()

# Using explicit configuration
config = DaytonaConfig(
    api_key="YOUR_API_KEY",
    api_url="https://app.daytona.io/api",
    target="us"
)
daytona = Daytona(config)
```

**Async:**

```python
import asyncio
from daytona import AsyncDaytona, DaytonaConfig

async def main():
    try:
        # Using environment variables (DAYTONA_API_KEY, DAYTONA_API_URL, DAYTONA_TARGET)
        daytona = AsyncDaytona()
        # Your async code here
        pass
    finally:
        await daytona.close()

    # Using explicit configuration
    config = DaytonaConfig(
        api_key="YOUR_API_KEY",
        api_url="https://app.daytona.io/api",
        target="us"
    )
    async with AsyncDaytona(config) as daytona:
        # Your code here
        pass

if __name__ == "__main__":
    asyncio.run(main())
```

For more information on configuring the Daytona SDK, see [API keys](../../SKILL.md#authentication#authentication).

## Async Python SDK

Daytona provides an additional `DAYTONA_HAPPY_EYEBALLS_DELAY` environment variable for HTTP transport tuning in the async Python SDK. Use it to reduce intermittent async connection failures, such as `aiohttp.ClientConnectorError`, that can occur on dual-stack (IPv4/IPv6) networks.

| Variable                           | Description                                                                 | Required |
| ---------------------------------- | --------------------------------------------------------------------------- | -------- |
| **`DAYTONA_HAPPY_EYEBALLS_DELAY`** | Controls **`aiohttp`** Happy Eyeballs (IPv4/IPv6 connection race) delay in seconds. | No       |

- unset or empty: use `aiohttp` default behavior
- `none` (case-insensitive): disable the IPv4/IPv6 race
- non-negative float (for example `0.25`): set an explicit delay in seconds

```bash
# Disable Happy Eyeballs
export DAYTONA_HAPPY_EYEBALLS_DELAY=none

# Or set an explicit delay in seconds
export DAYTONA_HAPPY_EYEBALLS_DELAY=0.25
```
