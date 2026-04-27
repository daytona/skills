## Contents

- Create volumes
- Mount volumes
- Work with volumes
- Get a volume by name
- List volumes
- Delete volumes
- Limitations
- Pricing & Limits
- See Also




Volumes are FUSE-based mounts that provide shared file access across Daytona Sandboxes. They enable sandboxes to read from large files instantly - no need to upload files manually to each sandbox. Volume data is stored in an S3-compatible object store.

- multiple volumes can be mounted to a single sandbox
- a single volume can be mounted to multiple sandboxes

## Create volumes

Daytona provides methods to create volumes using the [Daytona Dashboard ↗](https://app.daytona.io/dashboard/volumes) or programmatically using the Daytona [Python](../python-sdk/sync/volume.md), [TypeScript](../typescript-sdk/volume.md), [Ruby](../ruby-sdk/volume.md), [Go](./daytona.md#type-volumeservice), [Java](https://www.daytona.io/docs/en/java-sdk/volume-service) **SDKs**, [CLI](../cli.md#daytona-create), or [API](../api/README.md#daytona/tag/sandbox).

For persistent per-user, per-tenant, or per-workspace storage, use one shared volume per use case, environment, or project (for example a volume for staging and another for production), and set a dedicated `subpath` when you create each sandbox. The sandbox sees only that prefix inside the volume; it cannot access sibling subpaths.

This is the default pattern we recommend because it:

- stays within the per-organization volume [limits](#pricing--limits)
- avoids mounting a separate volume for every user or sandbox
- continues to provide strong isolation at the mount boundary

1. Navigate to [Daytona Volumes ↗](https://app.daytona.io/dashboard/volumes)
2. Click the **Create Volume** button
3. Enter the volume name

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
	volume, err := client.Volume.Create(context.Background(), "my-awesome-volume")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Volume ID: %s\n", volume.ID)
}
```

## Mount volumes

Daytona provides an option to mount a volume to a sandbox. Once a volume is created, it can be mounted to a sandbox by specifying it in the `CreateSandboxFromSnapshotParams` object. For per-user or multi-tenant data, pass `subpath` so only the specified folder inside the volume is visible at `mount_path`.

Mount the entire volume (omit `subpath`) when every sandbox that uses that volume should see the same tree, for example shared assets or single-tenant workloads.

Volume mount paths must meet the following requirements:

- **Must be absolute paths**: mount paths must start with `/` (e.g., `/home/daytona/volume`)
- **Cannot be root directory**: cannot mount to `/` or `//`
- **No relative path components**: cannot contain `/../`, `/./`, or end with `/..` or `/.`
- **No consecutive slashes**: cannot contain multiple consecutive slashes like `//` (except at the beginning)
- **Cannot mount to system directories**: the following system directories are prohibited: `/proc`, `/sys`, `/dev`, `/boot`, `/etc`, `/bin`, `/sbin`, `/lib`, `/lib64`

```go
import (
	"context"
	"log"

	"github.com/daytonaio/daytona/libs/sdk-go/pkg/daytona"
	"github.com/daytonaio/daytona/libs/sdk-go/pkg/types"
)

client, err := daytona.NewClient()
if err != nil {
	log.Fatal(err)
}

// Create a new volume or get an existing one
volume, err := client.Volume.Get(context.Background(), "my-awesome-volume")
if err != nil {
	// If volume doesn't exist, create it
	volume, err = client.Volume.Create(context.Background(), "my-awesome-volume")
	if err != nil {
		log.Fatal(err)
	}
}

mountDir := "/home/daytona/volume"

// Recommended for per-user / per-tenant data: one volume, unique subpath per sandbox
subpath := "users/alice"
sandbox, err := client.Create(context.Background(), types.SnapshotParams{
	SandboxBaseParams: types.SandboxBaseParams{
		Language: types.CodeLanguagePython,
		Volumes: []types.VolumeMount{
			{VolumeID: volume.ID, MountPath: mountDir, Subpath: &subpath},
		},
	},
})
if err != nil {
	log.Fatal(err)
}

// Entire volume at mount path (omit Subpath) when all sandboxes should share the same tree
_, err = client.Create(context.Background(), types.SnapshotParams{
	SandboxBaseParams: types.SandboxBaseParams{
		Language: types.CodeLanguagePython,
		Volumes: []types.VolumeMount{
			{VolumeID: volume.ID, MountPath: mountDir},
		},
	},
})
if err != nil {
	log.Fatal(err)
}
```

## Work with volumes

Daytona provides an option to read from and write to the volume just like any other directory in the sandbox file system. Files written to the volume persist beyond the lifecycle of any individual sandbox.

The following snippet demonstrate how to read from and write to a volume:

```go
import (
    "context"
    "log"
)

// Write to a file in the mounted volume
err := sandbox.FileSystem.UploadFile(context.Background(), []byte("Hello from Daytona volume!"), "/home/daytona/volume/example.txt")
if err != nil {
    log.Fatal(err)
}

// When you're done with the sandbox, you can remove it
// The volume will persist even after the sandbox is removed
err = sandbox.Delete(context.Background())
if err != nil {
	log.Fatal(err)
}
```

## Get a volume by name

Daytona provides an option to get a volume by its name.

```go
volume, err := client.Volume.Get(ctx, "my-awesome-volume")
```

## List volumes

Daytona provides an option to list all volumes.

```go
volumes, err := client.Volume.List(ctx)
```

## Delete volumes

Daytona provides an option to delete a volume. Deleted volumes cannot be recovered.

The following snippet demonstrate how to delete a volume:

```go
err := client.Volume.Delete(ctx, volume)
```

## Limitations

Since volumes are FUSE-based mounts, they can not be used for applications that require block storage access (like database tables). Volumes are generally slower for both read and write operations compared to the local sandbox file system.

## Pricing & Limits

Daytona volumes are included at no additional cost. Each organization can create up to 100 volumes, and volume data does not count against your storage quota.

You can view your current volume usage in the [Daytona Volumes ↗](https://app.daytona.io/dashboard/volumes).

## See Also
- [Python SDK - volumes](../python-sdk/volumes.md)
- [TypeScript SDK - volumes](../typescript-sdk/volumes.md)
