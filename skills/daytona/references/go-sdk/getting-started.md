## Contents

- Dashboard
- SDKs
- CLI
- API
- MCP server
- Multiple runtime support
- Guides
- Examples
- See Also




This section introduces core concepts, common workflows, and next steps for using Daytona.

## Dashboard

[Daytona Dashboard ↗](https://app.daytona.io/) is a visual user interface where you can manage sandboxes, access API keys, view usage, and more.
It serves as the primary point of control for managing your Daytona resources.

## SDKs

Daytona provides [Python](../python-sdk/README.md), [TypeScript](../typescript-sdk/README.md), [Ruby](../ruby-sdk/README.md), and [Go](./README.md) SDKs to programmatically interact with sandboxes. They support sandbox lifecycle management, code execution, resource access, and more.

## CLI

Daytona provides command-line access to core features for interacting with Daytona Sandboxes, including managing their lifecycle, snapshots, and more.

To interact with Daytona Sandboxes from the command line, install the Daytona CLI:

**Mac/Linux:**

```bash
brew install daytonaio/cli/daytona
```

**Windows:**

```bash
powershell -Command "irm https://get.daytona.io/windows | iex"
```

After installing the Daytona CLI, use the `daytona` command to interact with Daytona Sandboxes from the command line.

To upgrade the Daytona CLI to the latest version:

**Mac/Linux:**

```bash
brew upgrade daytonaio/cli/daytona
```

**Windows:**

```bash
powershell -Command "irm https://get.daytona.io/windows | iex"
```

To view all available commands and flags, see the [CLI reference](../cli.md).

## API

Daytona provides a RESTful API for interacting with Daytona Sandboxes, including managing their lifecycle, snapshots, and more.
It serves as a flexible and powerful way to interact with Daytona from your own applications.

To interact with Daytona Sandboxes from the API, see the [API reference](../api/README.md).

## MCP server

Daytona provides a Model Context Protocol (MCP) server that enables AI agents to interact with Daytona Sandboxes programmatically. The MCP server integrates with popular AI agents including Claude, Cursor, and Windsurf.

To set up the MCP server with your AI agent:

```bash
daytona mcp init [claude/cursor/windsurf]
```

For more information, see the [MCP server documentation](../platform/mcp.md).

## Multiple runtime support

Daytona supports multiple programming language runtimes for direct code execution inside the sandbox.

[TypeScript SDK](../typescript-sdk/README.md) works across multiple **JavaScript runtimes** including **Node.js**, **browsers**, and **serverless platforms**: Cloudflare Workers, AWS Lambda, Azure Functions, etc.

Using the Daytona SDK in browser-based environments or frameworks like [**Vite**](./getting-started.md#daytona-in-vite-projects) and [**Next.js**](./getting-started.md#daytona-in-nextjs-projects) requires configuring node polyfills.

### Daytona in Vite projects

When using Daytona SDK in a Vite-based project, configure node polyfills to ensure compatibility.

Add the following configuration to your `vite.config.ts` file in the `plugins` array:

```typescript
import { nodePolyfills } from 'vite-plugin-node-polyfills'

export default defineConfig({
  plugins: [
    // ... other plugins
    nodePolyfills({
      globals: { global: true, process: true, Buffer: true },
      overrides: {
        path: 'path-browserify-win32',
      },
    }),
  ],
  // ... rest of your config
})
```

### Daytona in Next.js projects

When using Daytona SDK in a Next.js project, configure node polyfills to ensure compatibility with Webpack and Turbopack bundlers.

Add the following configuration to your `next.config.ts` file:

```typescript
import type { NextConfig } from 'next'
import NodePolyfillPlugin from 'node-polyfill-webpack-plugin'
import { env, nodeless } from 'unenv'

const { alias: turbopackAlias } = env(nodeless, {})

const nextConfig: NextConfig = {
  // Turbopack
  experimental: {
    turbo: {
      resolveAlias: {
        ...turbopackAlias,
      },
    },
  },
  // Webpack
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.plugins.push(new NodePolyfillPlugin())
    }
    return config
  },
}

export default nextConfig
```

## Guides

Daytona provides a comprehensive set of guides to help you get started. The guides cover a wide range of topics, from basic usage to advanced topics, and showcase various types of integrations between Daytona and other tools.

For more information, see [guides](https://www.daytona.io/docs/en/guides).

## Examples

Daytona provides quick examples for common sandbox operations and best practices. <br />
The examples are based on the Daytona [Python SDK](../python-sdk/sync/process.md), [TypeScript SDK](../typescript-sdk/process.md), [Go SDK](./daytona.md#type-processservice), [Ruby SDK](../ruby-sdk/process.md), [CLI](../cli.md), and [API](../api/README.md) references. More examples are available in the [GitHub repository ↗](https://github.com/daytonaio/daytona/tree/main/examples).

### Create a sandbox

Create a [sandbox](./sandboxes.md) with default settings.

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/daytonaio/daytona/libs/sdk-go/pkg/daytona"
)

func main() {
    client, err := daytona.NewClient()
    if err != nil {
        log.Fatal(err)
    }

    sandbox, err := client.Create(context.Background(), nil)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("Sandbox ID: %s\n", sandbox.ID)
}
```

### Create and run code in a sandbox

Create a [sandbox](./sandboxes.md) and run code securely in it.

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/daytonaio/daytona/libs/sdk-go/pkg/daytona"
)

func main() {
    client, err := daytona.NewClient()
    if err != nil {
        log.Fatal(err)
    }

    sandbox, err := client.Create(context.Background(), nil)
    if err != nil {
        log.Fatal(err)
    }

    response, err := sandbox.Process.ExecuteCommand(context.Background(), "echo 'Hello, World!'")
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(response.Result)
    sandbox.Delete(context.Background())
}
```

### Create a sandbox with custom resources

Create a sandbox with [custom resources](./sandboxes.md#resources) (CPU, memory, disk).

```go
package main

import (
    "context"
    "log"

    "github.com/daytonaio/daytona/libs/sdk-go/pkg/daytona"
    "github.com/daytonaio/daytona/libs/sdk-go/pkg/types"
)

func main() {
    client, err := daytona.NewClient()
    if err != nil {
        log.Fatal(err)
    }

    sandbox, err := client.Create(context.Background(), types.ImageParams{
        Image: daytona.DebianSlim(nil),
        Resources: &types.Resources{
            CPU:    2,
            Memory: 4,
            Disk:   8,
        },
    })
    if err != nil {
        log.Fatal(err)
    }
}
```

### Create an ephemeral sandbox

Create an [ephemeral sandbox](./sandboxes.md#ephemeral-sandboxes) that is automatically deleted when stopped.

```go
package main

import (
    "context"
    "log"

    "github.com/daytonaio/daytona/libs/sdk-go/pkg/daytona"
    "github.com/daytonaio/daytona/libs/sdk-go/pkg/types"
)

func main() {
    client, err := daytona.NewClient()
    if err != nil {
        log.Fatal(err)
    }

    autoStop := 5
    sandbox, err := client.Create(context.Background(), types.SnapshotParams{
        SandboxBaseParams: types.SandboxBaseParams{
            Ephemeral:        true,
            AutoStopInterval: &autoStop,
        },
    })
    if err != nil {
        log.Fatal(err)
    }
}
```

### Create a sandbox from a snapshot

Create a sandbox from a pre-built [snapshot](./snapshots.md) for faster sandbox creation with pre-installed dependencies.

```go
package main

import (
    "context"
    "log"

    "github.com/daytonaio/daytona/libs/sdk-go/pkg/daytona"
    "github.com/daytonaio/daytona/libs/sdk-go/pkg/types"
)

func main() {
    client, err := daytona.NewClient()
    if err != nil {
        log.Fatal(err)
    }

    sandbox, err := client.Create(context.Background(), types.SnapshotParams{
        Snapshot: "my-snapshot-name",
        SandboxBaseParams: types.SandboxBaseParams{
            Language: types.CodeLanguagePython,
        },
    })
    if err != nil {
        log.Fatal(err)
    }
}
```

### Create a sandbox with a declarative image

Create a sandbox with a [declarative image](./declarative-builder.md) that defines dependencies programmatically.

```go
package main

import (
    "context"
    "log"

    "github.com/daytonaio/daytona/libs/sdk-go/pkg/daytona"
    "github.com/daytonaio/daytona/libs/sdk-go/pkg/types"
)

func main() {
    client, err := daytona.NewClient()
    if err != nil {
        log.Fatal(err)
    }

    image := daytona.DebianSlim(nil).
        PipInstall([]string{"requests", "pandas", "numpy"}).
        Workdir("/home/daytona")
    sandbox, err := client.Create(context.Background(), types.ImageParams{
        Image: image,
    })
    if err != nil {
        log.Fatal(err)
    }
}
```

### Create a sandbox with volumes

Create a sandbox with a [volume](./volumes.md) mounted to share data across sandboxes.

```go
package main

import (
    "context"
    "log"

    "github.com/daytonaio/daytona/libs/sdk-go/pkg/daytona"
    "github.com/daytonaio/daytona/libs/sdk-go/pkg/types"
)

func main() {
    client, err := daytona.NewClient()
    if err != nil {
        log.Fatal(err)
    }

    volume, err := client.Volume.Get(context.Background(), "my-volume")
    if err != nil {
        volume, err = client.Volume.Create(context.Background(), "my-volume")
        if err != nil {
            log.Fatal(err)
        }
    }

    sandbox, err := client.Create(context.Background(), types.SnapshotParams{
        SandboxBaseParams: types.SandboxBaseParams{
            Volumes: []types.VolumeMount{{
                VolumeID:  volume.ID,
                MountPath: "/home/daytona/data",
            }},
        },
    })
    if err != nil {
        log.Fatal(err)
    }
}
```

### Create a sandbox with a Git repository cloned

Create a sandbox with a [Git repository](../typescript-sdk/git.md) cloned to manage version control.

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/daytonaio/daytona/libs/sdk-go/pkg/daytona"
)

func main() {
    client, err := daytona.NewClient()
    if err != nil {
        log.Fatal(err)
    }

    sandbox, err := client.Create(context.Background(), nil)
    if err != nil {
        log.Fatal(err)
    }

    sandbox.Git.Clone(context.Background(), "https://github.com/daytonaio/daytona.git", "/home/daytona/daytona")
    status, err := sandbox.Git.Status(context.Background(), "/home/daytona/daytona")
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("Branch: %s\n", status.CurrentBranch)
}
```

## See Also
- [Python SDK - getting-started](../python-sdk/getting-started.md)
- [TypeScript SDK - getting-started](../typescript-sdk/getting-started.md)
