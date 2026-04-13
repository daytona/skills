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

```python
# Define a declarative image with python packages
declarative_image = (
  Image.debian_slim("3.12")
  .pip_install(["requests", "pytest"])
  .workdir("/home/daytona")
)

# Create a new sandbox with the declarative image and stream the build logs
sandbox = daytona.create(
  CreateSandboxFromImageParams(image=declarative_image),
  timeout=0,
  on_snapshot_create_logs=print,
)
```

## Create pre-built Snapshots

Daytona provides an option to [create pre-built snapshots](./snapshots.md#create-snapshots) that can be reused across multiple sandboxes.

The snapshot remains visible in the [Daytona Dashboard ↗](https://app.daytona.io/dashboard/snapshots) and is permanently cached, ensuring instant availability without rebuilding.

```python
# Create a python data science image
snapshot_name = "data-science-snapshot"

image = (
  Image.debian_slim("3.12")
  .pip_install(["pandas", "numpy"])
  .workdir("/home/daytona")
)

# Create the snapshot and stream the build logs
daytona.snapshot.create(
  CreateSnapshotParams(
    name=snapshot_name,
    image=image,
  ),
on_logs=print,
)

# Create a new sandbox using the pre-built snapshot
sandbox = daytona.create(
CreateSandboxFromSnapshotParams(snapshot=snapshot_name)
)
```

## Image configuration

Daytona provides an option to define images programmatically using the Daytona SDK. You can specify base images, install packages, add files, set environment variables, and more.

For a complete API reference and method signatures, see the [Python](./image.md), [TypeScript](../typescript-sdk/image.md), [Ruby](../ruby-sdk/image.md), and [Go](../go-sdk/daytona.md#type-DockerImage) SDK references.

### Base image selection

Daytona provides an option to select base images. The following snippets demonstrate how to select and configure base images:

```python
# Create an image from a base
image = Image.base("python:3.12-slim-bookworm")

# Use a Debian slim image with Python 3.12
image = Image.debian_slim("3.12")
```

### Package management

Daytona provides an option to install packages and dependencies to your image.
The following snippets demonstrate how to install packages and dependencies to your image:

```python
# Add pip packages
image = Image.debian_slim("3.12").pip_install(["requests", "pandas"])

# Install from requirements.txt
image = Image.debian_slim("3.12").pip_install_from_requirements("requirements.txt")

# Install from pyproject.toml (with optional dependencies)
image = Image.debian_slim("3.12").pip_install_from_pyproject("pyproject.toml", optional_dependencies=["dev"])
```

### File system operations

Daytona provides an option to add files and directories to your image.
The following snippets demonstrate how to add files and directories to your image:

```python
# Add a local file
image = Image.debian_slim("3.12").add_local_file("package.json", "/home/daytona/package.json")

# Add a local directory
image = Image.debian_slim("3.12").add_local_dir("src", "/home/daytona/src")
```

### Environment configuration

Daytona provides an option to configure environment variables and working directories.
The following snippets demonstrate how to configure environment variables and working directories:

```python
# Set environment variables
image = Image.debian_slim("3.12").env({"PROJECT_ROOT": "/home/daytona"})

# Set working directory
image = Image.debian_slim("3.12").workdir("/home/daytona")
```

### Commands and entrypoints

Daytona provides an option to execute commands during build and configure container startup behavior.
The following snippets demonstrate how to execute commands during build and configure container startup behavior:

```python
# Run shell commands during build
image = Image.debian_slim("3.12").run_commands(
    'apt-get update && apt-get install -y git',
    'groupadd -r daytona && useradd -r -g daytona -m daytona',
    'mkdir -p /home/daytona/workspace'
)

# Set entrypoint
image = Image.debian_slim("3.12").entrypoint(["/bin/bash"])

# Set default command
image = Image.debian_slim("3.12").cmd(["/bin/bash"])
```

### Dockerfile integration

Daytona provides an option to integrate existing Dockerfiles or add custom Dockerfile commands.
The following snippets demonstrate how to integrate existing Dockerfiles or add custom Dockerfile commands:

```python
# Add custom Dockerfile commands
image = Image.debian_slim("3.12").dockerfile_commands(["RUN echo 'Hello, world!'"])

# Use an existing Dockerfile
image = Image.from_dockerfile("Dockerfile")

# Extend an existing Dockerfile
image = Image.from_dockerfile("app/Dockerfile").pip_install(["numpy"])
```

## See Also
- [Python SDK - README](./README.md)
