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

Daytona provides volumes as a shared storage solution for sandboxes. To create a volume:

1. Navigate to [Daytona Volumes ↗](https://app.daytona.io/dashboard/volumes)
2. Click the **Create Volume** button
3. Enter the volume name

The following snippets demonstrate how to create a volume using the Daytona SDK:

```ruby
daytona = Daytona::Daytona.new
volume = daytona.volume.create("my-awesome-volume")
```

## Mount volumes

Daytona provides an option to mount a volume to a sandbox. Once a volume is created, it can be mounted to a sandbox by specifying it in the `CreateSandboxFromSnapshotParams` object. Volume mount paths must meet the following requirements:

- **Must be absolute paths**: Mount paths must start with `/` (e.g., `/home/daytona/volume`)
- **Cannot be root directory**: Cannot mount to `/` or `//`
- **No relative path components**: Cannot contain `/../`, `/./`, or end with `/..` or `/.`
- **No consecutive slashes**: Cannot contain multiple consecutive slashes like `//` (except at the beginning)
- **Cannot mount to system directories**: The following system directories are prohibited: `/proc`, `/sys`, `/dev`, `/boot`, `/etc`, `/bin`, `/sbin`, `/lib`, `/lib64`

The following snippets demonstrate how to mount a volume to a sandbox:

```ruby
require 'daytona'

daytona = Daytona::Daytona.new

# Create a new volume or get an existing one
volume = daytona.volume.get('my-volume', create: true)

# Mount the volume to the sandbox
mount_dir = '/home/daytona/volume'

params = Daytona::CreateSandboxFromSnapshotParams.new(
  language: Daytona::CodeLanguage::PYTHON,
  volumes: [DaytonaApiClient::SandboxVolume.new(volume_id: volume.id, mount_path: mount_dir)]
)
sandbox = daytona.create(params)

# Mount a specific subpath within the volume
# This is useful for isolating data or implementing multi-tenancy
params2 = Daytona::CreateSandboxFromSnapshotParams.new(
  language: Daytona::CodeLanguage::PYTHON,
  volumes: [DaytonaApiClient::SandboxVolume.new(
    volume_id: volume.id,
    mount_path: mount_dir,
    subpath: 'users/alice'
  )]
)
sandbox2 = daytona.create(params2)
```

## Work with volumes

Daytona provides an option to read from and write to the volume just like any other directory in the sandbox file system. Files written to the volume persist beyond the lifecycle of any individual sandbox.

The following snippet demonstrate how to read from and write to a volume:

```ruby
# Write to a file in the mounted volume using the Sandbox file system API
sandbox.fs.upload_file('Hello from Daytona volume!', '/home/daytona/volume/example.txt')

# When you're done with the sandbox, you can remove it
# The volume will persist even after the sandbox is removed
daytona.delete(sandbox)
```

For more information, see the [Python SDK](../python-sdk/README.md), [TypeScript SDK](../typescript-sdk/README.md), [Ruby SDK](./README.md), and [Go SDK](../go-sdk/README.md) references.

## Get a volume by name

Daytona provides an option to get a volume by its name.

```ruby
daytona = Daytona::Daytona.new
volume = daytona.volume.get('my-awesome-volume', create: true)
puts "#{volume.name} (#{volume.id})"
```

## List volumes

Daytona provides an option to list all volumes.

```ruby
daytona = Daytona::Daytona.new
volumes = daytona.volume.list
volumes.each do |volume|
  puts "#{volume.name} (#{volume.id})"
end
```

## Delete volumes

Daytona provides an option to delete a volume. Deleted volumes cannot be recovered.

The following snippet demonstrate how to delete a volume:

```ruby
volume = daytona.volume.get('my-volume', create: true)
daytona.volume.delete(volume)
```

## Limitations

Since volumes are FUSE-based mounts, they can not be used for applications that require block storage access (like database tables).
Volumes are generally slower for both read and write operations compared to the local sandbox file system.

## Pricing & Limits

Daytona Volumes are included at no additional cost. Each organization can create up to 100 volumes, and volume data does not count against your storage quota.

You can view your current volume usage in the [Daytona Dashboard ↗](https://app.daytona.io/dashboard/volumes).

## See Also
- [Ruby SDK - README](./README.md)
- [Python SDK - volumes](../python-sdk/volumes.md)
- [TypeScript SDK - volumes](../typescript-sdk/volumes.md)
- [Go SDK - volumes](../go-sdk/volumes.md)
