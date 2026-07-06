## Contents

- Create sandboxes
- Ephemeral sandboxes
- Linked sandboxes
- Start sandboxes
- Get sandbox
- List sandboxes
- Stop sandboxes
- Archive sandboxes
- Recover sandboxes
- Resize sandboxes
- Label sandboxes
- Create snapshot from sandbox
- Delete sandboxes
- Sandbox lifecycle
- Multiple runtime support
- Automated lifecycle management
- See Also




Daytona provides **full composable computers** — **sandboxes** — for AI agents.

Sandboxes are isolated runtime environments you can manage programmatically to run code. Each sandbox runs in isolation, giving it a dedicated kernel, filesystem, network stack, and allocated vCPU, RAM, and disk. Agents and developers get access to a full composable computer where they can install packages, run servers, compile code, and manage processes.

Sandboxes have **1 vCPU**, **1GB RAM**, and **3GiB disk** by default. Organizations get a maximum sandbox resource limit of **4 vCPUs**, **8GB RAM**, and **10GB disk**.

Sandboxes can use [snapshots](./snapshots.md) to capture a fully configured environment (base operating system, installed packages, dependencies and configuration) to create new sandboxes.

<DocLinkCardGrid>
  <DocLinkCard
    title="Container"
    href="#create-sandboxes"
    icon="package"
    description="Default Linux container runtime."
  />
  <DocLinkCard
    title="Linux"
    href="/docs/en/sandboxes/vm-sandboxes#linux-vm"
    icon="vm"
    description="Linux OS runtime in a virtual machine for running Linux-specific tools and workflows."
  />
  <DocLinkCard
    title="Windows"
    href="/docs/en/sandboxes/vm-sandboxes#windows"
    icon="vm"
    description="Windows OS runtime in a virtual machine for running Windows applications and tooling."
  />
  <DocLinkCard
    title="GPU"
    href="/docs/en/sandboxes/gpu-sandboxes"
    icon="gpu"
    description="NVIDIA GPU runtime for model inference, fine-tuning, and CUDA-accelerated compute."
  />
</DocLinkCardGrid>

## Create sandboxes

Create a sandbox.

1. Go to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click **Create Sandbox**
3. Click **Create**

```typescript
import { Daytona } from '@daytona/sdk'

const daytona = new Daytona()
const sandbox = await daytona.create()
```

### Snapshots

Create a sandbox from a [default snapshot](./snapshots.md#default-snapshots).

| **Snapshot**            | **vCPU** | **Memory** | **Storage** | **GPU** | **Sandbox Class** |
| ----------------------- | -------- | ---------- | ----------- | ------- | ----------------- |
| **`daytona-small`**     | 1        | 1GiB       | 3GiB        |         | Container         |
| **`daytona-medium`**    | 2        | 4GiB       | 8GiB        |         | Container         |
| **`daytona-large`**     | 4        | 8GiB       | 10GiB       |         | Container         |
| **`daytona-gpu`**       | 1        | 1GiB       | 1GiB        | 1       | GPU               |
| **`daytona-vm-small`**  | 1        | 1GiB       | 3GiB        |         | Linux VM          |
| **`daytona-vm-medium`** | 2        | 4GiB       | 8GiB        |         | Linux VM          |
| **`daytona-vm-large`**  | 4        | 8GiB       | 10GiB       |         | Linux VM          |
| **`windows-small`**     | 1        | 4GiB       | 30GiB       |         | Windows           |
| **`windows-medium`**    | 2        | 8GiB       | 50GiB       |         | Windows           |
| **`windows-large`**     | 4        | 16GiB      | 50GiB       |         | Windows           |

1. Go to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click **Create Sandbox**
3. Select a **`snapshot`**
4. Click **Create**

```typescript
import { Daytona } from '@daytona/sdk'

const daytona = new Daytona()
const sandbox = await daytona.create({
  snapshot: 'daytona-small',
})
```

### Resources

Sandboxes have **1 vCPU**, **1GB RAM**, and **3GiB disk** by default. Organizations get a maximum sandbox resource limit of **4 vCPUs**, **8GB RAM**, and **10GB disk**.

| **Resource** | **Unit** | **Default** | **Minimum** | **Maximum** |
| ------------ | -------- | ----------- | ----------- | ----------- |
| CPU          | vCPU     | **`1`**     | **`1`**     | **`4`**     |
| Memory       | GiB      | **`1`**     | **`1`**     | **`8`**     |
| Disk         | GiB      | **`3`**     | **`1`**     | **`10`**    |

1. Go to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click **Create Sandbox**
3. Enter a base **`image`**
4. Set **`resources`** (**`cpu`**, **`memory`**, **`disk`**) to the values within your organization's limits
5. Click **Create**

```typescript
import { Daytona, Image } from '@daytona/sdk'

const daytona = new Daytona()
const sandbox = await daytona.create({
  image: Image.base('ubuntu:22.04'),
  resources: { cpu: 2, memory: 4, disk: 8 },
})
```

## Ephemeral sandboxes

Create an ephemeral sandbox.

Ephemeral sandboxes are automatically deleted once they are stopped.

1. Go to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click **Create Sandbox**
3. Set **Ephemeral** to **`True`** or set the [auto-delete interval](#auto-delete-interval) to **`0`**
4. Click **Create**

```typescript
import { Daytona } from '@daytona/sdk'

const daytona = new Daytona()
const sandbox = await daytona.create({
  ephemeral: true,
  autoStopInterval: 5,
})
```

## Linked sandboxes

Create a linked sandbox.

Linked sandboxes are attached to an existing parent sandbox at creation time.

- **Lifecycle**

  Linked sandboxes are always ephemeral and cannot be persisted or resumed after stop. The [auto-delete interval](#auto-delete-interval) must be exactly `0` on create; this is enforced, not a default. The [auto-stop interval](#auto-stop-interval) sets the idle period in minutes after which the child sandbox stops. Once stopped, linked children are auto-deleted. Deleting the parent deletes all of its linked children (cascade). One parent may have many linked children (1:N).

- **Networking**

  Linked sandboxes share an internal link network. Connections work in both directions: the parent can reach each child and each child can reach the parent. Every sandbox on the link network is registered under its sandbox name and ID as DNS aliases, so either works as the host. For example: `telnet LINKED_SANDBOX_ID 5555` from the parent reaches port `5555` on the linked child sandbox.

1. Create a parent sandbox
2. Create one or more child sandboxes that reference the parent's sandbox ID. This records the relationship on the child sandbox as the linked sandbox ID. Omitting the linked sandbox parameter yields an unlinked sandbox.

```typescript
import { Daytona } from '@daytona/sdk'

const daytona = new Daytona()

const parent = await daytona.create()

const child = await daytona.create({
  linkedSandbox: parent.id,
  ephemeral: true,
})

// The link network registers each sandbox under its name as a DNS alias
const response = await child.process.executeCommand(
  `curl http://${parent.name}:3000/`
)
```

## Start sandboxes

Start a sandbox.

1. Go to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click the start icon (**▶**) next to the sandbox you want to start

```typescript
await sandbox.start()
```

## Get sandbox

Get a sandbox by ID or name.

```typescript
const sandbox = await daytona.get('my-sandbox-id-or-name')
```

## List sandboxes

List sandboxes.

```typescript
for await (const sandbox of daytona.list()) {
  console.log(sandbox.id)
}
```

## Stop sandboxes

Stop a sandbox.

Stopped sandboxes maintain filesystem persistence while their memory state is cleared. They incur only disk usage costs and can be started again when needed.

The stopped state should be used when a sandbox is expected to be started again. Otherwise, it is recommended to stop and then archive the sandbox to eliminate disk usage costs.

1. Go to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click the stop icon (**⏹**) next to the sandbox you want to stop

```typescript
await sandbox.stop()
```

If you need a faster shutdown, use force stop (`force=true` / `--force`) to terminate the sandbox immediately. Force stop is ungraceful and should be used when quick termination is more important than process cleanup. Avoid force stop for normal shutdowns where the process should flush buffers, write final state, or run cleanup hooks.

Common use cases for force stop include:

- you need to reduce stop time and can accept immediate termination
- the entrypoint ignores termination signals or hangs during shutdown

## Archive sandboxes

Archive a sandbox.

1. Ensure the sandbox is **stopped**
2. **Archive** the sandbox
3. Wait for the sandbox to reach the **archived** state to move filesystem state to object storage
4. **Start** the sandbox again when you need to use it

```typescript
await sandbox.archive()
```

## Recover sandboxes

Recover a sandbox.

1. Ensure the sandbox is in **error** state
2. Check that the sandbox is **recoverable**
3. Resolve any underlying issue that requires user intervention
4. **Recover** the sandbox and wait for it to be ready

```typescript
// Check if the sandbox is recoverable
if (sandbox.recoverable) {
  await sandbox.recover()
}
```

```typescript
await sandbox.recover()
```

## Resize sandboxes

Resize [sandbox resources](#resources) after creation.

On a running sandbox, you can increase CPU and memory without interruption. To decrease CPU or memory, or to increase disk capacity, stop the sandbox first. Disk size can only be increased and cannot be decreased.

Resizing updates the sandbox resource allocation (`cpu`, `memory`, and `disk`) for that sandbox only. CPU and memory control compute capacity for running workloads, while disk controls persistent filesystem capacity. Values must be integers and stay within your organization's per-sandbox resource limits.

1. Choose the new **CPU**, **memory**, and **disk** values within your organization's limits
2. Ensure the sandbox is **stopped** if you need to decrease CPU or memory, or increase disk
3. **Resize** the sandbox with the new resource values
4. **Start** the sandbox

```typescript
// Resize a started sandbox (CPU and memory can be increased)
await sandbox.resize({ cpu: 2, memory: 4 })

// Resize a stopped sandbox (CPU and memory can change, disk can only increase)
await sandbox.stop()
await sandbox.resize({ cpu: 4, memory: 8, disk: 20 })
await sandbox.start()
```

To verify CPU and memory limits inside the sandbox after resizing, read `cgroup` values directly. Tools such as `nproc`, `free`, `top`, `htop`, `/proc/cpuinfo`, and `/proc/meminfo` read host-level values and do not reflect sandbox resource limits.

```bash
cat /sys/fs/cgroup/cpu.max      # "<quota> <period>" (cores = quota / period)
cat /sys/fs/cgroup/memory.max   # bytes
df -h /                         # disk
```

## Label sandboxes

Set sandbox labels.

1. Go to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click **Create Sandbox**
3. Click **Add Labels**
4. Enter the labels in key-value pairs

```typescript
await sandbox.setLabels({
  team: 'platform',
  env: 'staging',
})
```

## Create snapshot from sandbox

Create a snapshot from an existing sandbox.

A snapshot captures a point-in-time copy of a sandbox that you can use as a base to create new sandboxes, templating a known-good environment for reuse.

Container sandboxes capture filesystem state only. For hot and cold snapshots on VM sandboxes (Linux and Windows), see [VM sandboxes](https://www.daytona.io/docs/en/sandboxes/vm-sandboxes).

```typescript
await sandbox._experimental_createSnapshot('my-sandbox-snapshot')
```

## Delete sandboxes

Delete a sandbox.

1. Go to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click the **Delete** button next to the sandbox you want to delete.

```typescript
await sandbox.delete()
```

## Sandbox lifecycle

A sandbox can have several different states. Each state reflects the status of your sandbox.

<Collapsible title="Sandbox states">

| **State**         | **Description**                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------- |
| Creating          | The sandbox is provisioning and will be ready to use.                                       |
| Pulling Snapshot  | The sandbox is pulling a [**snapshot**](./snapshots.md) to provide a base environment.  |
| Building Snapshot | The sandbox is building a [**snapshot**](./snapshots.md) to provide a base environment. |
| Pending Build     | The sandbox build is pending and will start shortly.                                        |
| Build Failed      | The sandbox build failed and needs to be retried.                                           |
| Starting          | The sandbox is starting and will be ready to use.                                           |
| Started           | The sandbox has started and is ready to use.                                                |
| Stopping          | The sandbox is stopping and will no longer accept requests.                                 |
| Stopped           | The sandbox has stopped and is no longer running.                                           |
| Pausing           | The sandbox is pausing while its filesystem and memory state are preserved.                 |
| Paused            | The sandbox is paused with its filesystem and memory state preserved.                       |
| Resuming          | The sandbox is resuming from a paused state and will be ready to use.                       |
| Archiving         | The sandbox is archiving and its state will be preserved.                                   |
| Archived          | The sandbox has been archived and its state is preserved.                                   |
| Restoring         | The sandbox is being restored from archive and will be ready to use shortly.                |
| Resizing          | The sandbox is being resized to a new set of resources.                                     |
| Snapshotting      | The sandbox is creating a [**snapshot**](./snapshots.md) of its filesystem and memory.  |
| Forking           | The sandbox is being forked into a new independent sandbox.                                 |
| Deleting          | The sandbox is deleting and will be removed.                                                |
| Deleted           | The sandbox has been deleted and no longer exists.                                          |
| Error             | The sandbox is in an error state and needs to be recovered.                                 |
| Unknown           | The default sandbox state before it is created.                                             |

</Collapsible>

The diagram demonstrates the states and possible transitions between them.


##### State transitions

A sandbox can transition between states in response to various actions. The following table lists the initial state, target state, and trigger for the transition.

<Collapsible title="State transitions">

| **Initial state** | **Target state**  | **Trigger**                                                                       |
| ----------------- | ----------------- | --------------------------------------------------------------------------------- |
| Unknown           | Pulling Snapshot  | The base snapshot is being pulled to provide the sandbox environment.             |
| Unknown           | Building Snapshot | The sandbox uses a declarative image build, which begins building.                |
| Pending Build     | Building Snapshot | The queued image build starts.                                                    |
| Building Snapshot | Build Failed      | The image build fails or times out.                                               |
| Pulling Snapshot  | Creating          | The snapshot is available and the sandbox container is created.                   |
| Building Snapshot | Creating          | The snapshot finishes building and the sandbox container is created.              |
| Creating          | Started           | The sandbox container finishes initializing and is running.                       |
| Stopped           | Starting          | A start is requested and the sandbox boots.                                       |
| Stopped           | Restoring         | A start is requested and the sandbox is restored from a backup.                   |
| Archived          | Restoring         | A start is requested and the archived filesystem is restored from object storage. |
| Restoring         | Started           | The restore completes and the sandbox is running.                                 |
| Starting          | Started           | The sandbox is running and ready to accept requests.                              |
| Started           | Stopping          | A stop is requested, or the auto-stop interval is exceeded.                       |
| Stopping          | Stopped           | The sandbox process exits and its memory state is cleared.                        |
| Started           | Pausing           | A pause is requested.                                                             |
| Pausing           | Paused            | The filesystem and memory state are preserved.                                    |
| Paused            | Resuming          | A start is requested on a paused sandbox.                                         |
| Paused            | Stopping          | A stop is requested on a paused sandbox.                                          |
| Resuming          | Started           | The sandbox resumes from memory and is running.                                   |
| Stopped           | Archiving         | An archive is requested, or the auto-archive interval is exceeded.                |
| Archiving         | Archived          | The backup completes and the filesystem is moved to object storage.               |
| Started           | Resizing          | CPU or memory is increased on a running sandbox.                                  |
| Stopped           | Resizing          | Resources are changed on a stopped sandbox.                                       |
| Resizing          | Started           | The running sandbox returns to service after resizing.                            |
| Resizing          | Stopped           | The stopped sandbox completes resizing.                                           |
| Started           | Snapshotting      | A snapshot of the filesystem and memory is created.                               |
| Stopped           | Snapshotting      | A snapshot of the filesystem is created.                                          |
| Snapshotting      | Started           | The snapshot completes and the sandbox returns to service.                        |
| Snapshotting      | Stopped           | The snapshot completes and the sandbox remains stopped.                           |
| Started           | Forking           | The sandbox is forked into a new independent sandbox.                             |
| Forking           | Started           | The fork completes and the sandbox returns to service.                            |
| Started           | Deleting          | A delete is requested, or the auto-delete interval is exceeded.                   |
| Stopped           | Deleting          | A delete is requested.                                                            |
| Archived          | Deleted           | An archived sandbox is deleted directly without being restored.                   |
| Deleting          | Deleted           | The sandbox is removed and its resources are released.                            |
| Started           | Error             | An operation fails or times out.                                                  |
| Error             | Restoring         | A recover is requested for a recoverable error and the sandbox is restored.       |
| Error             | Archiving         | An errored sandbox with a completed backup is archived to preserve its state.     |

</Collapsible>

## Multiple runtime support

Daytona sandboxes support Python, TypeScript, and JavaScript programming language runtimes for direct code execution inside the sandbox. The `language` parameter controls which programming language runtime is used for the sandbox:

- **`python`**
- **`typescript`**
- **`javascript`**

If omitted, the Daytona SDK will default to `python`. To override this, explicitly set the `language` value when creating the sandbox.

## Automated lifecycle management

Sandboxes can be automatically stopped, archived, and deleted based on user-defined intervals. The intervals act as a TTL (time-to-live) mechanism for the sandbox. You can also refresh the last activity timestamp to explicitly signal activity when lifecycle behavior depends on inactivity intervals.

### Update sandbox last activity

Update a sandbox's last activity timestamp.

This updates the sandbox's recorded activity time without changing its runtime state. It is useful when your workflow is driven by external systems or background orchestration that may not reset inactivity tracking.

```typescript
await sandbox.refreshActivity()
```

### Auto-stop interval

The auto-stop interval sets the amount of time after which a running sandbox is automatically stopped. The auto-stop triggers even if there are internal processes running in the sandbox.

1. Go to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click **Create Sandbox**
3. Set **`auto-stop`** interval to the desired value in minutes
    - **`0`**: disables the auto-stop functionality, allowing the sandbox to run indefinitely
    - if not set, the default interval of 15 minutes is used
4. Click **Create**

```typescript
const sandbox = await daytona.create({
  snapshot: 'my-snapshot-name',
  // Disables the auto-stop feature - default is 15 minutes
  autoStopInterval: 0,
})
```

The system differentiates between "internal processes" and "active user interaction". Merely having a script or background task running is not sufficient to keep the sandbox alive.

##### What resets the timer

The inactivity timer resets only for specific external interactions:

- Updates to [sandbox lifecycle states](#sandbox-lifecycle)
- Network requests through [sandbox previews](./preview.md)
- Active [SSH connections](./ssh-access.md)
- API requests to the [Daytona Toolbox SDK](../api/README.md#daytona-toolbox)

##### What does not reset the timer

The following do not reset the timer:

- SDK requests that are not toolbox actions
- Background scripts (e.g., `npm run dev` run as a fire-and-forget command)
- Long-running tasks without external interaction
- Processes that don't involve active monitoring

If you run a long-running task like LLM inference that takes more than 15 minutes to complete without any external interaction, the sandbox may auto-stop mid-process because the process itself doesn't count as "activity", therefore the timer is not reset.

### Auto-archive interval

The auto-archive interval sets the amount of time after which a continuously stopped sandbox is automatically archived.

1. Go to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click **Create Sandbox**
3. Set **`auto-archive`** interval to the desired value in minutes
    - **`0`**: the maximum interval of 30 days is used
    - if not set, the default interval of 7 days is used
4. Click **Create**

```typescript
const sandbox = await daytona.create({
  snapshot: 'my-snapshot-name',
  // Auto-archive after a sandbox has been stopped for 1 hour
  autoArchiveInterval: 60,
})
```

### Auto-delete interval

The auto-delete interval sets the amount of time after which a continuously stopped sandbox is automatically deleted.

1. Go to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click **Create Sandbox**
3. Set **`auto-delete`** to the desired value in minutes
    - `-1`: disables the auto-delete functionality
    - `0`: the sandbox is deleted immediately after it is stopped
    - if not set, the sandbox is not deleted automatically
4. Click **Create**

```typescript
const sandbox = await daytona.create({
  snapshot: 'my-snapshot-name',
  // Auto-delete after a sandbox has been stopped for 1 hour
  autoDeleteInterval: 60,
})

// Delete the sandbox immediately after it has been stopped
await sandbox.setAutoDeleteInterval(0)

// Disable auto-deletion
await sandbox.setAutoDeleteInterval(-1)
```

### Running indefinitely

Run sandboxes indefinitely.

By default, Daytona sandboxes auto-stop after 15 minutes of inactivity. To keep a sandbox running without interruption, set the auto-stop interval to `0` when creating a new sandbox.

1. Go to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click **Create Sandbox**
3. Set **`auto-stop`** to **`0`**
4. Click **Create**

```typescript
const sandbox = await daytona.create({
  snapshot: 'my_awesome_snapshot',
  // Disables the auto-stop feature - default is 15 minutes
  autoStopInterval: 0,
})
```

## See Also
- [Python SDK - sandboxes](../python-sdk/sandboxes.md)
