## Contents

- Snapshot lifecycle
- Create Snapshots
- Get a Snapshot by name
- List Snapshots
- Activate Snapshots
- Deactivate Snapshots
- Delete Snapshots
- Run Docker in a Sandbox
- Run Kubernetes in a Sandbox
- Default Snapshots
- See Also




Snapshots are sandbox templates created from [Docker](https://www.docker.com/) or [OCI](https://opencontainers.org/) compatible images. Sandboxes can use a [default snapshot](#default-snapshots) or custom snapshots to provide a consistent and reproducible sandbox environments for your dependencies, settings, and resources.

Daytona supports running [Docker](#run-docker-in-a-sandbox) and [Kubernetes](#run-kubernetes-in-a-sandbox) workloads inside sandboxes using snapshots.

## Snapshot lifecycle

Throughout the snapshot lifecycle, a snapshot can have the following states:

| **State**          | **Description**                                 |
| ------------------ | ----------------------------------------------- |
| **`pending`**      | Snapshot creation requested                     |
| **`building`**     | Snapshot is being built                         |
| **`pulling`**      | Snapshot image is being pulled from a registry  |
| **`active`**       | Snapshot is ready to use for creating sandboxes |
| **`inactive`**     | Snapshot is deactivated                         |
| **`error`**        | Snapshot creation failed                        |
| **`build_failed`** | Snapshot build process failed                   |
| **`removing`**     | Snapshot is being deleted                       |
> **Note:**
> Inactive snapshots cannot be used to create sandboxes. They must be explicitly [re-activated](#activate-snapshots) before use. When activated, the snapshot returns to `pending` state and is re-processed before becoming `active` again.

## Create Snapshots

Daytona provides methods to create snapshots using the [Daytona Dashboard ↗](https://app.daytona.io/dashboard/snapshots) or programmatically using the Daytona [Python](../python-sdk/sync/snapshot.md), [TypeScript](../typescript-sdk/snapshot.md), [Ruby](../ruby-sdk/snapshot.md), [Go](./daytona.md#SnapshotService) **SDKs**, [CLI](../cli.md#daytona-snapshot), or [API](../api/README.md#daytona/tag/snapshots).

Snapshots can be created using:

- [public images](#using-public-images)
- [local images](#using-local-images)
- [images from private registries](#using-images-from-private-registries)
- [the declarative builder](#using-the-declarative-builder)

1. Navigate to [Daytona Snapshots ↗](https://app.daytona.io/dashboard/snapshots)
2. Click the **Create Snapshot** button
3. Enter the **snapshot name**, **image** (tag or digest), **entrypoint**, and **resources**

- **Snapshot name**: Identifier used to reference the snapshot in the SDK or CLI.
- **Image**: Base image for the snapshot. Must include either a tag or a digest (e.g., **`ubuntu:22.04`**). The **`latest`** tag is not allowed. Since images tagged `latest` get frequent updates, only specific tags are supported. Same applies to tags such as `lts` or `stable`, and we recommend avoiding those when defining an image to prevent unexpected behavior.
- **Entrypoint** (optional): The entrypoint command for the snapshot. Ensure that the entrypoint is a long-running command. If not provided, or if the snapshot does not have an entrypoint, `sleep infinity` will be used as the default.
- [**Resources**](./sandboxes.md#resources) (optional): The resources you want the underlying Sandboxes to have. By default, Daytona Sandboxes use **1 vCPU**, **1GiB memory**, and **3GiB storage**.

**Python:**

```python
image = Image.debian_slim('3.12').pip_install('numpy')
daytona.snapshot.create(
    CreateSnapshotParams(name='my-awesome-snapshot', image=image),
    on_logs=lambda chunk: print(chunk, end=""),
)
```

**TypeScript:**

```typescript
const image = Image.debianSlim('3.12').pipInstall('numpy');
await daytona.snapshot.create({ name: 'my-awesome-snapshot', image: image }, { onLogs: console.log });
```

**Ruby:**

```ruby
image = Image.debian_slim('3.12').pip_install('numpy')
params = CreateSnapshotParams.new(name: 'my-awesome-snapshot', image: image)
snapshot = daytona.snapshot.create(params) do |chunk|
  print chunk
end
```

**Go:**

```go
// Create from Docker Hub image
snapshot, logChan, err := client.Snapshots.Create(ctx, &types.CreateSnapshotParams{
    Name:  "my-awesome-snapshot",
    Image: "python:3.11-slim",
})
if err != nil {
    return err
}

// Stream build logs
for log := range logChan {
    fmt.Println(log)
}

// Create with custom image and resources
image := daytona.Base("python:3.11").PipInstall([]string{"numpy"})
snapshot, logChan, err := client.Snapshots.Create(ctx, &types.CreateSnapshotParams{
    Name:  "my-awesome-snapshot",
    Image: image,
    Resources: &types.Resources{CPU: 2, Memory: 4096},
})
```

**CLI:**

```bash
daytona snapshot create my-awesome-snapshot --image python:3.11-slim --cpu 2 --memory 4
```

**API:**

```bash
curl https://app.daytona.io/api/snapshots \
  --request POST \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer YOUR_SECRET_TOKEN' \
  --data '{
    "name": "my-awesome-snapshot",
    "imageName": "python:3.11-slim",
    "cpu": 2,
    "memory": 4
  }'
```

### Using public images

Daytona supports creating snapshots from any publicly accessible image or container registry.

1. Navigate to [Daytona Snapshots ↗](https://app.daytona.io/dashboard/snapshots)
2. Click the **Create Snapshot** button
3. Enter the **snapshot name** and **image** (tag or digest) of any publicly accessible image or container registry

Once the snapshot is pulled, validated, and has an `Active` state, it is ready to be used.

**Python:**

```python
daytona.snapshot.create(
    CreateSnapshotParams(name='my-awesome-snapshot', image='python:3.11-slim'),
    on_logs=lambda chunk: print(chunk, end=""),
)
```

**TypeScript:**

```typescript
await daytona.snapshot.create({ name: 'my-awesome-snapshot', image: 'python:3.11-slim' }, { onLogs: console.log });
```

**Ruby:**

```ruby
params = CreateSnapshotParams.new(name: 'my-awesome-snapshot', image: 'python:3.11-slim')
snapshot = daytona.snapshot.create(params) do |chunk|
  print chunk
end
```

**Go:**

```go
snapshot, logChan, err := client.Snapshots.Create(ctx, &types.CreateSnapshotParams{
    Name:  "my-awesome-snapshot",
    Image: "python:3.11-slim",
})
if err != nil {
    return err
}

// Stream build logs
for log := range logChan {
    fmt.Println(log)
}
```

**CLI:**

```bash
daytona snapshot create my-awesome-snapshot --image python:3.11-slim
```

**API:**

```bash
curl https://app.daytona.io/api/snapshots \
  --request POST \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer YOUR_SECRET_TOKEN' \
  --data '{
    "name": "my-awesome-snapshot",
    "imageName": "python:3.11-slim"
  }'
```

For more information, see the [Python SDK](../python-sdk/sync/snapshot.md), [TypeScript SDK](../typescript-sdk/snapshot.md), [Ruby SDK](../ruby-sdk/snapshot.md), [Go SDK](./daytona.md#SnapshotService.Create), [CLI](../cli.md#daytona-snapshot), and [API](../api/README.md#daytona/tag/snapshots) references.

> [**create (Python SDK)**](../python-sdk/sync/snapshot.md#snapshotservicecreate)
>
> [**create (TypeScript SDK)**](../typescript-sdk/snapshot.md#create)
>
> [**create (Ruby SDK)**](../ruby-sdk/snapshot.md#create)
>
> [**create (Go SDK)**](./daytona.md#SnapshotService.Create)
>
> [**create (CLI)**](../cli.md#daytona-snapshot-create)
>
> [**create (API)**](../api/README.md#daytona/tag/snapshots/POST/snapshots)

### Using local images

Daytona supports creating snapshots from local images or from local Dockerfiles. To create a snapshot from a local image or from a local Dockerfile, use the [Daytona CLI](../cli.md#daytona-snapshot).

Daytona expects the local image to be built for AMD64 architecture. Therefore, the `--platform=linux/amd64` flag is required when building the Docker image if your machine is running on a different architecture.

1. Ensure the image and tag you want to use is available

```bash
docker images
```

2. Create a snapshot and push it to Daytona:

```bash
daytona snapshot push custom-alpine:3.21 --name alpine-minimal
```
> **Tip:**
> Use the flags `--cpu`, `--memory` and `--disk` to specify the [resources](./sandboxes.md#resources) you want the underlying sandboxes to have. Example:
> <br />
> ```bash
> daytona snapshot push custom-alpine:3.21 --name alpine-minimal --cpu 2 --memory 4 --disk 8
> ```

Alternatively, use the `--dockerfile` flag under `create` to pass the path to the Dockerfile you want to use and Daytona will build the snapshot for you. The `COPY`/`ADD` commands will be automatically parsed and added to the context. To manually add files to the context, use the `--context` flag.

```bash
daytona snapshot create my-awesome-snapshot --dockerfile ./Dockerfile
```

```text
Building image from /Users/user/docs/Dockerfile
Step 1/5 : FROM alpine:latest

...
 ⡿  Waiting for the Snapshot to be validated ...
...

 ✓  Use 'harbor-transient.internal.daytona.app/daytona/trying-daytona:0.0.1' to create a new sandbox using this Snapshot
```

### Using images from private registries

Daytona supports creating snapshots from images from [Docker Hub](#docker-hub), [Google Artifact Registry](#google-artifact-registry), [GitHub Container Registry](#github-container-registry) or other private container registries.

1. Navigate to [Daytona Registries ↗](https://app.daytona.io/dashboard/registries)
2. Click the **Add Registry** button
3. Enter the **registry name**, **registry URL**, **username**, **password**, and **project** (if applicable)
4. After the container registry is successfully created, navigate to [Daytona Snapshots ↗](https://app.daytona.io/dashboard/snapshots)
5. Click the **Create Snapshot** button
6. Enter the **snapshot name** and private **image** (tag or digest). When creating the snapshot, make sure to input the entire private image name, including the registry location and project name (e.g. **`my-private-registry.com/<my-project>/custom-alpine:3.21`**)

Optionally, set the **`CreateSandboxFromSnapshotParams`** field to use the custom snapshot.

#### Docker Hub

Daytona supports creating snapshots from Docker Hub images.

1. Navigate to [Daytona Registries ↗](https://app.daytona.io/dashboard/registries)
2. Click the **Add Registry** button
3. Enter the **registry name**, **registry URL**, **username**, **password**, and **project** (if applicable)

- **Registry URL**: `docker.io`
- **Username**: Docker Hub username (the account with access to the image)
- **Password**: [Docker Hub Personal Access Token](https://docs.docker.com/docker-hub/access-tokens/) (not your account password)
- **Create the Snapshot**: `docker.io/<username>/<image>:<tag>`

4. After the container registry is successfully created, navigate to [Daytona Snapshots ↗](https://app.daytona.io/dashboard/snapshots)
5. Click the **Create Snapshot** button
6. Enter the **snapshot name** and **image** (tag or digest). When creating the snapshot, input the entire image name, including the registry location and project name (e.g. **`docker.io/<username>/<image>:<tag>`**)

#### Google Artifact Registry

Daytona supports creating snapshots from images from Google Artifact Registry.

To use an image from Google Artifact Registry, configure the registry using a [service account key](https://cloud.google.com/iam/docs/keys-create-delete) in JSON format.

1. Navigate to [Daytona Registries ↗](https://app.daytona.io/dashboard/registries)
2. Click the **Add Registry** button
3. Enter the **registry name**, **registry URL**, **username**, **password**, and **project** (if applicable)

- **Registry URL**: base URL for your region (e.g., `https://us-central1-docker.pkg.dev` or `https://us-central1-docker.pkg.dev/your-org`).
- **Username**: `_json_key`
- **Password**: Paste the full contents of your Service Account JSON key file
- **Project**: Google Cloud Project ID
- **Create the Snapshot**: `us-central1-docker.pkg.dev/<project>/<repo>/<image>:<tag>`

4. After the container registry is successfully created, navigate to [Daytona Snapshots ↗](https://app.daytona.io/dashboard/snapshots)
5. Click the **Create Snapshot** button
6. Enter the **snapshot name** and **image** (tag or digest). When creating the snapshot, make sure to input the entire image name, including the registry location and project name (e.g. **`us-central1-docker.pkg.dev/<project>/<repo>/<image>:<tag>`**)

#### GitHub Container Registry (GHCR)

Daytona supports creating snapshots from images from GitHub Container Registry (GHCR).

1. Navigate to [Daytona Registries ↗](https://app.daytona.io/dashboard/registries)
2. Click the **Add Registry** button
3. Enter the **registry name**, **registry URL**, **username**, **password**, and **project** (if applicable)

- **Registry URL**: `ghcr.io`
- **Username**: GitHub username (the account with access to the image)
- **Password**: [GitHub Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) (not your account password). Personal access token (PAT) requires **`write:packages`**, **`read:packages`**, and **`delete:packages`** scopes.

4. After the container registry is successfully created, navigate to [Daytona Snapshots ↗](https://app.daytona.io/dashboard/snapshots)
5. Click the **Create Snapshot** button
6. Enter the **snapshot name** and **image** (tag or digest). When creating the snapshot, make sure to input the entire image name, including the registry location and project name (e.g. **`ghcr.io/<my-project>/custom-alpine:3.21`**)

#### Amazon Elastic Container Registry (ECR)

Daytona supports creating snapshots from images from Amazon Elastic Container Registry.

1. Navigate to [Daytona Registries ↗](https://app.daytona.io/dashboard/registries)
2. Click the **Add Registry** button
3. Enter the **registry name**, **registry URL**, **username**, **password**, and **project** (if applicable)

- **Registry URL**: `<account_id>.dkr.ecr.<region>.amazonaws.com`
- **Username**: `AWS`
- **Password**: [Authorization token](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html)

4. After the container registry is successfully created, navigate to [Daytona Snapshots ↗](https://app.daytona.io/dashboard/snapshots)
5. Click the **Create Snapshot** button
6. Enter the **snapshot name** and **image** (tag or digest). When creating the snapshot, make sure to input the entire image name, including the registry location and repository name (e.g. **`123456789012.dkr.ecr.us-east-1.amazonaws.com/my-repo/custom-alpine:3.21`**)
> **Caution:**
> Amazon ECR authorization tokens expire after **12 hours**. Update the registry password in Daytona each time the token expires. Support for automatic renewal is coming soon.

### Using the declarative builder

[Declarative Builder](./declarative-builder.md) provides a powerful, code-first approach to defining dependencies for Daytona Sandboxes. Instead of importing images from a container registry, you can programmatically define them using the Daytona [SDKs](./getting-started.md#sdks).

### Resources

Snapshots can be customized with specific resource requirements. By default, Daytona Sandboxes use **1 vCPU**, **1GB RAM**, and **3GiB disk**. For more information, see [sandbox resources](./sandboxes.md#resources).

To view your available resources and limits, see [limits](../platform/limits.md) or navigate to [Daytona Limits ↗](https://app.daytona.io/dashboard/limits).

Snapshot resources can be customized using the `Resources` class.

```go
// Create a snapshot with custom resources
image := daytona.Base("python:3.11").PipInstall([]string{"numpy"})
snapshot, logChan, err := client.Snapshots.Create(ctx, &types.CreateSnapshotParams{
    Name:      "my-awesome-snapshot",
    Image:     image,
    Resources: &types.Resources{CPU: 2, Memory: 4, Disk: 8},
})
if err != nil {
    return err
}

// Stream build logs
for log := range logChan {
    fmt.Println(log)
}
```

### Regions

When creating a snapshot, you can specify the [region](./regions.md) in which it will be available. If not specified, the snapshot will be created in your organization's default region.

When you later create a sandbox from this snapshot, you can use the snapshot's region as the target region for the sandbox.


## Get a Snapshot by name

Daytona provides an option to get a snapshot by name.

The following snippet returns the snapshot with the specified name:

```go
snapshot, err := client.Snapshots.Get(ctx, "my-awesome-snapshot")
if err != nil {
    return err
}
fmt.Printf("%s (%s)\n", snapshot.Name, snapshot.ImageName)
```

## List Snapshots

Daytona provides options to list snapshots and view their details.

The following snippet lists all snapshots on the first page with a limit of 10 snapshots per page.

```go
// List first page with default limit
result, err := client.Snapshots.List(ctx, nil, nil)
if err != nil {
    return err
}

// List with pagination
page, limit := 2, 10
result, err := client.Snapshots.List(ctx, &page, &limit)
fmt.Printf("Page %d of %d, total: %d\n", result.Page, result.TotalPages, result.Total)
```

For more information, see the [Python SDK](../python-sdk/sync/snapshot.md), [TypeScript SDK](../typescript-sdk/snapshot.md), [Ruby SDK](../ruby-sdk/snapshot.md), [Go SDK](./daytona.md#SnapshotService.List), [CLI](../cli.md#daytona-snapshot-list), and [API](../api/README.md#daytona/tag/snapshots) references.

> [**list (Python SDK)**](../python-sdk/sync/snapshot.md#snapshotservicelist)
>
> [**list (TypeScript SDK)**](../typescript-sdk/snapshot.md#list)
>
> [**list (Ruby SDK)**](../ruby-sdk/snapshot.md#list)
>
> [**list (Go SDK)**](./daytona.md#SnapshotService.List)
>
> [**list (CLI)**](../cli.md#daytona-snapshot-list)
>
> [**list (API)**](../api/README.md#daytona/tag/snapshots/GET/snapshots)

## Activate Snapshots

Snapshots automatically become inactive after 2 weeks of not being used. To activate an inactive snapshot:

1. Navigate to [Daytona Snapshots ↗](https://app.daytona.io/dashboard/snapshots)
2. Click the three dots at the end of the row for the snapshot you want to activate
3. Click the **Activate** button


## Deactivate Snapshots

Daytona provides an option to deactivate snapshots. Deactivated snapshots are not available for new sandboxes.

1. Navigate to [Daytona Snapshots ↗](https://app.daytona.io/dashboard/snapshots)
2. Click the three dots at the end of the row for the snapshot you want to deactivate
3. Click the **Deactivate** button

## Delete Snapshots

Daytona provides options to delete snapshots. Deleted snapshots cannot be recovered.

1. Navigate to [Daytona Snapshots ↗](https://app.daytona.io/dashboard/snapshots)
2. Click the three dots at the end of the row for the snapshot you want to delete
3. Click the **Delete** button

```go
snapshot, err := client.Snapshots.Get(ctx, "my-awesome-snapshot")
if err != nil {
    return err
}
err = client.Snapshots.Delete(ctx, snapshot)
if err != nil {
    return err
}
fmt.Println("Snapshot deleted")
```

## Run Docker in a Sandbox

Daytona Sandboxes can run Docker containers inside them (**Docker-in-Docker**), enabling you to build, test, and deploy containerized applications. This is particularly useful when your projects have dependencies on external services like databases, message queues, or other microservices.

Agents can seamlessly interact with these services since they run within the same sandbox environment, providing better isolation and security compared to external service dependencies. The following use cases are supported:

- Run databases (PostgreSQL, Redis, MySQL) and other services
- Build and test containerized applications
- Deploy microservices and their dependencies
- Create isolated development environments with full container orchestration
> **Note:**
> Docker-in-Docker Sandboxes require additional resources due to the Docker daemon overhead. Consider allocating at least 2 vCPU and 4GiB of memory for optimal performance.

### Create a Docker-in-Docker Snapshot

Daytona provides an option to create a snapshot with Docker support using pre-built Docker-in-Docker images as a base or by manually installing Docker in a custom image.

#### Using pre-built images

The following base images are widely used for creating Docker-in-Docker snapshots or can be used as a base for a custom Dockerfile:

- `docker:28.3.3-dind`: official Docker-in-Docker image (Alpine-based, lightweight)
- `docker:28.3.3-dind-rootless`: rootless Docker-in-Docker for enhanced security
- `docker:28.3.2-dind-alpine3.22`: Docker-in-Docker image with Alpine 3.22

#### Using manual installation

Alternatively, install Docker manually in a custom Dockerfile:

```dockerfile
FROM ubuntu:22.04
# Install Docker using the official install script
RUN curl -fsSL https://get.docker.com | VERSION=28.3.3 sh -
```

### Run Docker Compose in a Sandbox

Docker Compose allows you to define and run multi-container applications. With Docker-in-Docker enabled in a Daytona Sandbox, you can use Docker Compose to orchestrate services like databases, caches, and application containers.

First, create a Docker-in-Docker snapshot using the [Daytona Dashboard ↗](https://app.daytona.io/dashboard/snapshots) or [CLI](../cli.md#daytona-snapshot-create) with one of the [pre-built images](#using-pre-built-images) (e.g., `docker:28.3.3-dind`). Then use the following snippet to run Docker Compose services inside a sandbox:

```go
package main

import (
	"context"
	"fmt"

	"github.com/daytonaio/sdk-go/daytona"
	"github.com/daytonaio/sdk-go/types"
)

func main() {
	ctx := context.Background()

	// Initialize the Daytona client
	client, _ := daytona.NewDaytona(nil)

	// Create a sandbox from a Docker-in-Docker snapshot
	sandbox, _ := client.Create(ctx, &types.CreateSandboxFromSnapshotParams{
		Snapshot: daytona.Ptr("docker-dind"),
	}, nil)

	// Create a docker-compose.yml file
	composeContent := `
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
`
	sandbox.Fs.UploadFile(ctx, []byte(composeContent), "docker-compose.yml")

	// Start Docker Compose services
	result, _ := sandbox.Process.ExecuteCommand(ctx, "docker compose -p demo up -d", nil)
	fmt.Println(result.Result)

	// Check running services
	result, _ = sandbox.Process.ExecuteCommand(ctx, "docker compose -p demo ps", nil)
	fmt.Println(result.Result)

	// Clean up
	sandbox.Process.ExecuteCommand(ctx, "docker compose -p demo down", nil)
}
```

## Run Kubernetes in a Sandbox

Daytona Sandboxes can run a Kubernetes cluster inside the sandbox. Kubernetes runs entirely inside the sandbox and is removed when the sandbox is deleted, keeping environments secure and reproducible.

### Run k3s in a Sandbox

The following snippet installs and starts a k3s cluster inside a sandbox and lists all running pods.

```typescript
import { Daytona } from '@daytona/sdk'
import { setTimeout } from 'timers/promises'

// Initialize the Daytona client
const daytona = new Daytona()

// Create the sandbox instance
const sandbox = await daytona.create()

// Run the k3s installation script
const response = await sandbox.process.executeCommand(
  'curl -sfL https://get.k3s.io | sh -'
)

// Run k3s
const sessionName = 'k3s-server'
await sandbox.process.createSession(sessionName)
const k3s = await sandbox.process.executeSessionCommand(sessionName, {
  command: 'sudo /usr/local/bin/k3s server',
  async: true,
})

// Give time to k3s to fully start
await setTimeout(30000)

// Get all pods
const pods = await sandbox.process.executeCommand(
  'sudo /usr/local/bin/kubectl get pod -A'
)
console.log(pods.result)
```

## Default Snapshots

When a sandbox is created with no snapshot specified, Daytona uses a default snapshot that includes `python`, `node`, their language servers, and several common pip packages. Daytona provides three default snapshot sizes:

| **Snapshot**         | **vCPU** | **Memory** | **Storage** |
| -------------------- | -------- | ---------- | ----------- |
| **`daytona-small`**  | 1        | 1GiB       | 3GiB        |
| **`daytona-medium`** | 2        | 4GiB       | 8GiB        |
| **`daytona-large`**  | 4        | 8GiB       | 10GiB       |

All default snapshots are based on the `daytonaio/sandbox:<version>` image. For more information, see the [Dockerfile](https://github.com/daytonaio/daytona/blob/main/images/sandbox/Dockerfile).

### Python packages (pip)

- `anthropic` (v0.76.0)
- `beautifulsoup4` (v4.14.3)
- `claude-agent-sdk` (v0.1.22)
- `daytona` (v0.134.0)
- `django` (v6.0.1)
- `flask` (v3.1.2)
- `huggingface-hub` (v0.36.0)
- `instructor` (v1.14.4)
- `keras` (v3.13.0)
- `langchain` (v1.2.7)
- `llama-index` (v0.14.13)
- `matplotlib` (v3.10.8)
- `numpy` (v2.4.1)
- `ollama` (v0.6.1)
- `openai` (v2.15.0)
- `opencv-python` (v4.13.0.90)
- `pandas` (v2.3.3)
- `pillow` (v12.1.0)
- `pydantic-ai` (v1.47.0)
- `requests` (v2.32.5)
- `scikit-learn` (v1.8.0)
- `scipy` (v1.17.0)
- `seaborn` (v0.13.2)
- `sqlalchemy` (v2.0.46)
- `torch` (v2.10.0)
- `transformers` (v4.57.6)

### Node.js packages (npm)

- `@anthropic-ai/claude-code` (v2.1.19)
- `bun` (v1.3.6)
- `openclaw` (v2026.2.1)
- `opencode-ai` (v1.1.35)
- `ts-node` (v10.9.2)
- `typescript` (v5.9.3)
- `typescript-language-server` (v5.1.3)

## See Also
- [Go SDK - daytona#SnapshotService.Create](./daytona.md#SnapshotService.Create)
- [Go SDK - daytona#SnapshotService.Delete](./daytona.md#SnapshotService.Delete)
- [Go SDK - daytona#SnapshotService.Get](./daytona.md#SnapshotService.Get)
- [Python SDK - snapshots](../python-sdk/snapshots.md)
- [TypeScript SDK - snapshots](../typescript-sdk/snapshots.md)
