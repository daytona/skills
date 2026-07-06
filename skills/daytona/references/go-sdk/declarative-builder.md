## Contents

- Build declarative images
- Image configuration
- See Also




Declarative Builder provides a powerful, code-first approach to defining dependencies for Daytona Sandboxes. Instead of importing images from a container registry, you can programmatically define them using the Daytona SDK.

The declarative builder system supports two primary workflows:

- [**Declarative images**](#build-declarative-images): build images on demand when creating sandboxes
- [**Pre-built snapshots**](#create-pre-built-snapshots): create and register ready-to-use [snapshots](./snapshots.md)

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

## Image configuration

Daytona provides an option to define images programmatically. Chain the methods below to build a complete image definition in a single fluent call.

1. **Select a base image**

    Start from any registry image with `Image.base()`, or use `Image.debian_slim()` for a Python-ready Debian image.

2. **Install Python packages**

    Add packages with `pip_install()`, or install from `requirements.txt` or `pyproject.toml` using `pip_install_from_requirements()` and `pip_install_from_pyproject()`.

3. **Add files and directories**

    Copy local files into the image with `add_local_file()` and `add_local_dir()`.

4. **Configure environment**

    Set environment variables and the working directory with `env()` and `workdir()`.

5. **Install system packages**

    Use `run_commands()` to install OS-level CLI tools and libraries not available through `pip`. Chain `apt-get update`, install, and cache cleanup with `&&` in a single command to minimize Docker layers.

6. **Add additional runtimes**

    Install secondary language runtimes in a single chained `RUN` instruction. The example below adds Node.js 20 alongside Python.

7. **Set up a non-root user**

    Run all installation steps as `root` first, then create the user, fix ownership of the working directory, and switch with the `USER` directive. Commands that write to system locations after switching users will fail with permission errors.

8. **Configure startup**

    Set the container entrypoint and default command with `entrypoint()` and `cmd()`.

```go
version := "3.12"
// 1. Base image
image := daytona.DebianSlim(&version).
  // 2. Python packages
  PipInstall([]string{"requests", "pandas"}).
  // 3. Local files
  AddLocalFile("package.json", "/home/daytona/package.json").
  AddLocalDir("src", "/home/daytona/src").
  // 4. Environment
  Env("PROJECT_ROOT", "/home/daytona").
  Workdir("/home/daytona").
  // 5. System packages
  AptGet([]string{"git", "curl", "ffmpeg", "jq"}).
  // 6. Additional runtime
  Run("apt-get update " +
    "&& apt-get install -y --no-install-recommends curl ca-certificates " +
    "&& curl -fsSL https://deb.nodesource.com/setup_20.x | bash - " +
    "&& apt-get install -y nodejs " +
    "&& rm -rf /var/lib/apt/lists/*").
  // 7. Non-root user
  Run("groupadd -r daytona && useradd -r -g daytona -m -d /home/daytona daytona").
  Run("chown -R daytona:daytona /home/daytona").
  User("daytona").
  // 8. Startup
  Entrypoint([]string{"/bin/bash"}).
  Cmd([]string{"/bin/bash"})
```

### Dockerfile integration

Integrate Dockerfiles and custom Dockerfile commands.

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
- [Python SDK - declarative-builder](../python-sdk/declarative-builder.md)
- [TypeScript SDK - declarative-builder](../typescript-sdk/declarative-builder.md)
