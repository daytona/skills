## Contents

- Build declarative images
- Create pre-built Snapshots
- Image configuration
- See Also




Declarative Builder provides a powerful, code-first approach to defining dependencies for Daytona Sandboxes. Instead of importing images from a container registry, you can programmatically define them using the Daytona SDK.

The declarative builder system supports two primary workflows:

1. [**Declarative images**](#declarative-image-building): build images with varying dependencies _on demand_ when creating sandboxes
2. [**Pre-built Snapshots**](#creating-pre-built-snapshots): create and register _ready-to-use_ [Snapshots](./snapshots.md) that can be shared across multiple sandboxes

## Build declarative images

Daytona provides an option to create declarative images on-the-fly when creating sandboxes. This is ideal for iterating quickly without creating separate snapshots.

Declarative images are cached for 24 hours, and are automatically reused when running the same script. Thus, subsequent runs on the same runner will be almost instantaneous.

```go
// Define a declarative image with python packages
version := "3.12"
declarativeImage := daytona.DebianSlim(&version).
  PipInstall([]string{"requests", "pytest"}).
  Workdir("/home/daytona")

// Create a new sandbox with the declarative image and stream the build logs
logChan := make(chan string)
go func() {
  for log := range logChan {
    fmt.Print(log)
  }
}()

sandbox, err := client.Create(ctx, types.ImageParams{
  Image: declarativeImage,
}, options.WithTimeout(0), options.WithLogChannel(logChan))
if err != nil {
  // handle error
}
```

## Create pre-built Snapshots

Daytona provides an option to [create pre-built snapshots](./snapshots.md#create-snapshots) that can be reused across multiple sandboxes.

The snapshot remains visible in the [Daytona Dashboard ↗](https://app.daytona.io/dashboard/snapshots) and is permanently cached, ensuring instant availability without rebuilding.

```go
// Create a python data science image
snapshotName := "data-science-snapshot"

version := "3.12"
image := daytona.DebianSlim(&version).
  PipInstall([]string{"pandas", "numpy"}).
  Workdir("/home/daytona")

// Create the snapshot and stream the build logs
_, logChan, err := client.Snapshot.Create(ctx, &types.CreateSnapshotParams{
  Name:  snapshotName,
  Image: image,
})
if err != nil {
  // handle error
}
for log := range logChan {
  fmt.Print(log)
}

// Create a new sandbox using the pre-built snapshot
sandbox, err := client.Create(ctx, types.SnapshotParams{
  Snapshot: snapshotName,
})
if err != nil {
  // handle error
}
```

## Image configuration

Daytona provides an option to define images programmatically using the Daytona SDK. You can specify base images, install packages, add files, set environment variables, and more.

For a complete API reference and method signatures, see the [Python](../python-sdk/image.md), [TypeScript](../typescript-sdk/image.md), [Ruby](../ruby-sdk/image.md), and [Go](./daytona.md#type-DockerImage) SDK references.

### Base image selection

Daytona provides an option to select base images. The following snippets demonstrate how to select and configure base images:

```go
// Create an image from a base
image := daytona.Base("python:3.12-slim-bookworm")

// Use a Debian slim image with Python 3.12
version := "3.12"
image := daytona.DebianSlim(&version)
```

### Package management

Daytona provides an option to install packages and dependencies to your image.
The following snippets demonstrate how to install packages and dependencies to your image:

```go
// Add pip packages
version := "3.12"
image := daytona.DebianSlim(&version).PipInstall([]string{"requests", "pandas"})

// Install from requirements.txt
image := daytona.DebianSlim(&version).
  AddLocalFile("requirements.txt", "/tmp/requirements.txt").
  Run("pip install -r /tmp/requirements.txt")

// Install from pyproject.toml (with optional dependencies)
image := daytona.DebianSlim(&version).
  AddLocalFile("pyproject.toml", "/tmp/pyproject.toml").
  Run("pip install /tmp[dev]")
```

### File system operations

Daytona provides an option to add files and directories to your image.
The following snippets demonstrate how to add files and directories to your image:

```go
// Add a local file
version := "3.12"
image := daytona.DebianSlim(&version).AddLocalFile("package.json", "/home/daytona/package.json")

// Add a local directory
image := daytona.DebianSlim(&version).AddLocalDir("src", "/home/daytona/src")
```

### Environment configuration

Daytona provides an option to configure environment variables and working directories.
The following snippets demonstrate how to configure environment variables and working directories:

```go
// Set environment variables
version := "3.12"
image := daytona.DebianSlim(&version).Env("PROJECT_ROOT", "/home/daytona")

// Set working directory
image := daytona.DebianSlim(&version).Workdir("/home/daytona")
```

### Commands and entrypoints

Daytona provides an option to execute commands during build and configure container startup behavior.
The following snippets demonstrate how to execute commands during build and configure container startup behavior:

```go
// Run shell commands during build
version := "3.12"
image := daytona.DebianSlim(&version).
  Run("apt-get update && apt-get install -y git").
  Run("groupadd -r daytona && useradd -r -g daytona -m daytona").
  Run("mkdir -p /home/daytona/workspace")

// Set entrypoint
image := daytona.DebianSlim(&version).Entrypoint([]string{"/bin/bash"})

// Set default command
image := daytona.DebianSlim(&version).Cmd([]string{"/bin/bash"})
```

### Dockerfile integration

Daytona provides an option to integrate existing Dockerfiles or add custom Dockerfile commands.
The following snippets demonstrate how to integrate existing Dockerfiles or add custom Dockerfile commands:

```go
// Note: In Go, FromDockerfile takes the Dockerfile content as a string
content, err := os.ReadFile("Dockerfile")
if err != nil {
  // handle error
}
image := daytona.FromDockerfile(string(content))

// Extend an existing Dockerfile with additional commands
content, err = os.ReadFile("app/Dockerfile")
if err != nil {
  // handle error
}
image := daytona.FromDockerfile(string(content)).
  PipInstall([]string{"numpy"})
```

## See Also
- [Go SDK - README](./README.md)
- [Python SDK - declarative-builder](../python-sdk/declarative-builder.md)
- [TypeScript SDK - declarative-builder](../typescript-sdk/declarative-builder.md)
