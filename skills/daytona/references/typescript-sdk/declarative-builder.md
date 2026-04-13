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

```typescript
// Define a declarative image with python packages
const declarativeImage = Image.debianSlim('3.12')
  .pipInstall(['requests', 'pytest'])
  .workdir('/home/daytona')

// Create a new sandbox with the declarative image and stream the build logs
const sandbox = await daytona.create(
  {
    image: declarativeImage,
  },
  {
    timeout: 0,
    onSnapshotCreateLogs: console.log,
  }
)
```

## Create pre-built Snapshots

Daytona provides an option to [create pre-built snapshots](./snapshots.md#create-snapshots) that can be reused across multiple sandboxes.

The snapshot remains visible in the [Daytona Dashboard ↗](https://app.daytona.io/dashboard/snapshots) and is permanently cached, ensuring instant availability without rebuilding.

```typescript
// Create a python data science image
const snapshotName = 'data-science-snapshot'

const image = Image.debianSlim('3.12')
  .pipInstall(['pandas', 'numpy'])
  .workdir('/home/daytona')

// Create the snapshot and stream the build logs
await daytona.snapshot.create(
  {
    name: snapshotName,
    image,
  },
  {
    onLogs: console.log,
  }
)

// Create a new sandbox using the pre-built snapshot
const sandbox = await daytona.create({
  snapshot: snapshotName,
})
```

## Image configuration

Daytona provides an option to define images programmatically using the Daytona SDK. You can specify base images, install packages, add files, set environment variables, and more.

For a complete API reference and method signatures, see the [Python](../python-sdk/image.md), [TypeScript](./image.md), [Ruby](../ruby-sdk/image.md), and [Go](../go-sdk/daytona.md#type-DockerImage) SDK references.

### Base image selection

Daytona provides an option to select base images. The following snippets demonstrate how to select and configure base images:

```typescript
// Create an image from a base
const image = Image.base('python:3.12-slim-bookworm')

// Use a Debian slim image with Python 3.12
const image = Image.debianSlim('3.12')
```

### Package management

Daytona provides an option to install packages and dependencies to your image.
The following snippets demonstrate how to install packages and dependencies to your image:

```typescript
// Add pip packages
const image = Image.debianSlim('3.12').pipInstall(['requests', 'pandas'])

// Install from requirements.txt
const image = Image.debianSlim('3.12').pipInstallFromRequirements('requirements.txt')

// Install from pyproject.toml (with optional dependencies)
const image = Image.debianSlim('3.12').pipInstallFromPyproject('pyproject.toml', {
  optionalDependencies: ['dev']
})
```

### File system operations

Daytona provides an option to add files and directories to your image.
The following snippets demonstrate how to add files and directories to your image:

```typescript
// Add a local file
const image = Image.debianSlim('3.12').addLocalFile('package.json', '/home/daytona/package.json')

// Add a local directory
const image = Image.debianSlim('3.12').addLocalDir('src', '/home/daytona/src')
```

### Environment configuration

Daytona provides an option to configure environment variables and working directories.
The following snippets demonstrate how to configure environment variables and working directories:

```typescript
// Set environment variables
const image = Image.debianSlim('3.12').env({ PROJECT_ROOT: '/home/daytona' })

// Set working directory
const image = Image.debianSlim('3.12').workdir('/home/daytona')
```

### Commands and entrypoints

Daytona provides an option to execute commands during build and configure container startup behavior.
The following snippets demonstrate how to execute commands during build and configure container startup behavior:

```typescript
// Run shell commands during build
const image = Image.debianSlim('3.12').runCommands(
    'apt-get update && apt-get install -y git',
    'groupadd -r daytona && useradd -r -g daytona -m daytona',
    'mkdir -p /home/daytona/workspace'
)

// Set entrypoint
const image = Image.debianSlim('3.12').entrypoint(['/bin/bash'])

// Set default command
const image = Image.debianSlim('3.12').cmd(['/bin/bash'])
```

### Dockerfile integration

Daytona provides an option to integrate existing Dockerfiles or add custom Dockerfile commands.
The following snippets demonstrate how to integrate existing Dockerfiles or add custom Dockerfile commands:

```typescript
// Add custom Dockerfile commands
const image = Image.debianSlim('3.12').dockerfileCommands(['RUN echo "Hello, world!"'])

// Use an existing Dockerfile
const image = Image.fromDockerfile('Dockerfile')

// Extend an existing Dockerfile
const image = Image.fromDockerfile("app/Dockerfile").pipInstall(['numpy'])
```

## See Also
- [TypeScript SDK - README](./README.md)
- [Python SDK - declarative-builder](../python-sdk/declarative-builder.md)
