## Contents

- Create Sandboxes
- Start Sandboxes
- Get Sandbox
- List Sandboxes
- Stop Sandboxes
- Pause Sandboxes
- Archive Sandboxes
- Recover Sandboxes
- Resize Sandboxes
- Fork Sandboxes
- Label Sandboxes
- Create Snapshot from Sandbox
- Delete Sandboxes
- Sandbox lifecycle
- Multiple runtime support
- Automated lifecycle management
- See Also




Daytona provides **full composable computers** — **sandboxes** — for AI agents. Sandboxes are isolated runtime environments you can manage programmatically to run code. Each sandbox runs in isolation, giving it a dedicated kernel, filesystem, network stack, and allocated vCPU, RAM, and disk. Agents get access to a full composable computer environment where they can install packages, run servers, compile code, and manage processes.

Sandboxes have **1 vCPU**, **1GB RAM**, and **3GiB disk** by default. [Organizations](../platform/organizations.md) get a maximum sandbox resource limit of **4 vCPUs**, **8GB RAM**, and **10GB disk**. For more power, see [resources](#resources) or contact [support@daytona.io](mailto:support@daytona.io).

Sandboxes use [snapshots](./snapshots.md) to capture a fully configured environment (base OS, installed packages, dependencies, and configuration) to create new sandboxes.

Each sandbox has its own network stack with per-sandbox firewall rules. By default, sandboxes follow standard network policies, but you can restrict egress to a specific set of allowed destinations or block all outbound traffic entirely. For more details, see [network limits](./network-limits.md).

- **Sandbox SDKs**: [TypeScript](../typescript-sdk/sandbox.md), [Python](../python-sdk/sync/sandbox.md), [Ruby](../ruby-sdk/sandbox.md), [Go](./daytona.md#type-sandbox), [Java](https://www.daytona.io/docs/en/java-sdk/sandbox)
- **Sandbox API**: [RESTful API](../api/README.md#daytona/tag/sandbox) ([OpenAPI spec](https://www.daytona.io/docs/en/openapi.json)), [Toolbox API](../api/README.md#daytona-toolbox) ([OpenAPI spec](https://www.daytona.io/docs/en/toolbox-openapi.json))
- **Sandbox CLI**: [Mac/Linux/Windows](../cli.md)

## Create Sandboxes

Daytona provides methods to create sandboxes.

1. Navigate to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click **Create Sandbox**
3. Click **Create** to create a sandbox

```go
package main

import (
	"context"
	"github.com/daytonaio/daytona/libs/sdk-go/pkg/daytona"
)

func main() {
	client, _ := daytona.NewClient()
	ctx := context.Background()
	_, _ = client.Create(ctx, nil)
}
```

### GPU Sandboxes
> **Caution: Experimental**
> This feature is experimental. To request access, contact [support@daytona.io](mailto:support@daytona.io).

Daytona provides methods to create GPU sandboxes.

Daytona supports NVIDIA GPU devices for sandbox creation. This allows you to run GPU workloads such as model inference, fine-tuning, and CUDA-accelerated compute inside a sandbox.

Each GPU sandbox is ephemeral and supports up to **16 vCPUs**, **192GB RAM**, and **512GB disk**.

1. Navigate to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click **Create Sandbox**
3. Select a GPU snapshot
4. Click **Create** to create a GPU sandbox

To create a GPU sandbox programmatically, use the pre-built `daytona-gpu` snapshot, target `us-east-1` region, and set `auto_delete_interval` to `0` (ephemeral).

```go
package main

import (
	"context"
	"github.com/daytonaio/daytona/libs/sdk-go/pkg/daytona"
	"github.com/daytonaio/daytona/libs/sdk-go/pkg/types"
)

func main() {
	client, _ := daytona.NewClientWithConfig(&types.DaytonaConfig{
		Target: "us-east-1",
	})
	ctx := context.Background()
	params := types.SnapshotParams{
		Snapshot: "daytona-gpu",
		SandboxBaseParams: types.SandboxBaseParams{
			Ephemeral: true,
		},
	}
	_, _ = client.Create(ctx, params)
}
```

### Ephemeral Sandboxes

Daytona provides methods to create ephemeral sandboxes.

Ephemeral sandboxes are automatically deleted once they are stopped. They are useful for short-lived tasks or testing purposes.

To create an ephemeral sandbox, set the `ephemeral` parameter to `True` when creating a sandbox. Setting [**`autoDeleteInterval: 0`**](#auto-delete-interval) (ephemeral) has the same effect.

```go
package main

import (
	"context"
	"github.com/daytonaio/daytona/libs/sdk-go/pkg/daytona"
	"github.com/daytonaio/daytona/libs/sdk-go/pkg/types"
)

func main() {
	client, _ := daytona.NewClient()
	ctx := context.Background()

	autoStopInterval := 5 // delete after 5 minutes of inactivity
	params := types.SnapshotParams{
		SandboxBaseParams: types.SandboxBaseParams{
			Language:         types.CodeLanguagePython,
			Ephemeral:        true,
			AutoStopInterval: &autoStopInterval,
		},
	}
	_, _ = client.Create(ctx, params)
}
```

### Resources

Sandboxes have **1 vCPU**, **1GB RAM**, and **3GiB disk** by default. Organizations get a maximum sandbox resource limit of **4 vCPUs**, **8GB RAM**, and **10GB disk**.

| **Resource** | **Unit** | **Default** | **Minimum** | **Maximum** |
| ------------ | -------- | ----------- | ----------- | ----------- |
| CPU          | vCPU     | **`1`**     | **`1`**     | **`4`**     |
| Memory       | GiB      | **`1`**     | **`1`**     | **`8`**     |
| Disk         | GiB      | **`3`**     | **`1`**     | **`10`**    |

To set custom sandbox resources, use the `Resources` class. All resource parameters are optional and must be integers. If not specified, Daytona will use the default values. Maximum values are per-sandbox limits set at the organization level.

```go
package main

import (
	"context"
	"github.com/daytonaio/daytona/libs/sdk-go/pkg/daytona"
	"github.com/daytonaio/daytona/libs/sdk-go/pkg/types"
)

func main() {
	client, _ := daytona.NewClient()
	ctx := context.Background()
	_, _ = client.Create(ctx, types.ImageParams{
		Image: "python:3.12",
		Resources: &types.Resources{
			CPU:    2,
			Memory: 4,
			Disk:   8,
		},
	})
}
```

## Start Sandboxes

Daytona provides methods to start sandboxes.

1. Navigate to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click the start icon (**▶**) next to the sandbox you want to start

```go
sandbox.Start(ctx)
```

## Get Sandbox

Daytona provides methods to get a sandbox by ID or name.

```go
sandbox, err := client.Get(ctx, "my-sandbox-id-or-name")
```

## List Sandboxes

Daytona provides methods to list sandboxes.

```go
iter := client.List(ctx, nil)
defer iter.Close()
for iter.Next() {
    sandbox := iter.Value()
    fmt.Println(sandbox.ID)
}
if err := iter.Err(); err != nil {
    log.Fatal(err)
}
```

##### Sandbox details page

[Daytona Dashboard ↗](https://app.daytona.io/dashboard/) provides a sandbox details page to view detailed information about a sandbox and interact with it directly.

1. Navigate to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click on a sandbox you want to view the details of
3. Click **View** to open the sandbox details page

The sandbox details page provides a summary of the sandbox information and actions to perform on the sandbox:

- **Name**: the name of the sandbox
- **UUID**: the unique identifier of the sandbox
- **State**: the sandbox state with a visual indicator
- **Actions**: [start](#start-sandboxes), [stop](#stop-sandboxes), [recover](#recover-sandboxes), [archive](#archive-sandboxes), [delete](#delete-sandboxes), refresh, [SSH access](./ssh-access.md), [screen recordings](./computer-use-guide.md#screen-recording)
- [**Region**](./regions.md): the target region where the sandbox is running
- [**Snapshot**](./snapshots.md): the snapshot used to create the sandbox
- [**Resources**](#resources): allocated sandbox CPU, memory, and disk
- [**Lifecycle**](#sandbox-lifecycle): [auto-stop](#auto-stop-interval), [auto-archive](#auto-archive-interval), and [auto-delete](#auto-delete-interval) intervals
- **Labels**: key-value pairs assigned to the sandbox
- **Timestamps**: when the sandbox was created and when the last event occurred
- [**Web terminal**](../platform/web-terminal.md): an embedded web terminal session directly in the browser
- **Filesystem**: sandbox filesystem tree for viewing and managing files and directories: create, upload, download, copy, refresh, collapse, search, and delete capabilities
- [**VNC**](./vnc-access.md): a graphical desktop session for sandboxes that have a desktop environment
- [**Logs**](https://www.daytona.io/docs/en/observability/otel-collection): a detailed record of user and system activity for the sandbox
- **Metrics**: sandbox metrics data displayed as charts
- **Traces**: distributed traces and spans collected from the sandbox
- **Spending**: usage and cost over time

## Stop Sandboxes

Daytona provides methods to stop sandboxes.

Stopped sandboxes maintain filesystem persistence while their memory state is cleared. They incur only disk usage costs and can be started again when needed.

The stopped state should be used when a sandbox is expected to be started again. Otherwise, it is recommended to stop and then archive the sandbox to eliminate disk usage costs.

1. Navigate to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click the stop icon (**⏹**) next to the sandbox you want to stop

```go
sandbox.Stop(ctx)
```

If you need a faster shutdown, use force stop (`force=true` / `--force`) to terminate the sandbox immediately. Force stop is ungraceful and should be used when quick termination is more important than process cleanup. Avoid force stop for normal shutdowns where the process should flush buffers, write final state, or run cleanup hooks.

Common use cases for force stop include:

- you need to reduce stop time and can accept immediate termination
- the entrypoint ignores termination signals or hangs during shutdown

## Pause Sandboxes
> **Caution: Experimental**
> This feature is experimental. To request access, contact [support@daytona.io](mailto:support@daytona.io).

Daytona provides methods to pause sandboxes.

Pausing a sandbox keeps both filesystem state and memory persistence, so sandboxes can resume from in-memory runtime state. Compared to regular stop behavior, pause is useful for workloads with active in-memory context and state continuity.

Daytona supports pause functionality through VM-based runners. Pause is handled through the existing stop action. This means stop behaves as pause and preserves memory state, while force stop performs a full shutdown without preserving memory state.

## Archive Sandboxes

Daytona provides methods to archive sandboxes.

A sandbox must be stopped before it can be archived. When a sandbox is archived, the entire filesystem state is moved to a cost-effective object storage, making it available for an extended period.

Starting an archived sandbox takes more time than starting a stopped sandbox, depending on its size. It can be started again in the same way as a stopped sandbox.

```go
sandbox.Archive(ctx)
```

## Recover Sandboxes

Daytona provides methods to recover sandboxes.


##### Recover from error state

When a sandbox enters an error state, it can sometimes be recovered using the `recover` method, depending on the underlying error reason. The `recoverable` flag indicates whether the error state can be resolved through an automated recovery procedure.

Recovery actions are not performed automatically because they address errors that require **further user intervention**, such as freeing up storage space.


## Resize Sandboxes

Daytona provides methods to resize [sandbox resources](#resources) after creation.

On a running sandbox, you can increase CPU and memory without interruption. To decrease CPU or memory, or to increase disk capacity, stop the sandbox first. Disk size can only be increased and cannot be decreased.

Resizing updates the sandbox resource allocation (`cpu`, `memory`, and `disk`) for that sandbox only. CPU and memory control compute capacity for running workloads, while disk controls persistent filesystem capacity. Values must be integers and stay within your organization's per-sandbox resource limits.

```go
// Resize a started sandbox (CPU and memory can be increased)
err := sandbox.Resize(ctx, &types.Resources{CPU: 2, Memory: 4})

// Resize a stopped sandbox (CPU and memory can change, disk can only increase)
err = sandbox.Stop(ctx)
err = sandbox.Resize(ctx, &types.Resources{CPU: 4, Memory: 8, Disk: 20})
err = sandbox.Start(ctx)
```

To verify CPU and memory limits inside the sandbox after resizing, read `cgroup` values directly. Tools such as `nproc`, `free`, `top`, `htop`, `/proc/cpuinfo`, and `/proc/meminfo` read host-level values and do not reflect sandbox resource limits.

```bash
cat /sys/fs/cgroup/cpu.max      # "<quota> <period>" (cores = quota / period)
cat /sys/fs/cgroup/memory.max   # bytes
df -h /                         # disk
```

## Fork Sandboxes
> **Caution: Experimental**
> This feature is experimental. To request access, contact [support@daytona.io](mailto:support@daytona.io).

Daytona provides methods to fork sandboxes.

Forking creates a duplicate of your sandbox's filesystem and memory, and copies it into a new sandbox. The new sandbox is fully independent: it can be started, stopped, and deleted without affecting the original. The sandbox must be in started state before forking.

Daytona tracks the parent-child relationship in a fork tree, so you can always trace a fork's lineage back to the sandbox it was created from. You can fork a fork, building out branches as needed. The parent sandbox cannot be deleted while it has active fork children.

1. Navigate to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click the three-dot menu (**⋮**) next to the sandbox you want to fork
3. Select **Fork**

```go
// Fork sandbox through the Sandbox instance
name := "my-forked-sandbox"
forkedSandbox, err := sandbox.ExperimentalFork(ctx, &name)
if err != nil {
    return err
}
```

To view the fork tree for a sandbox and all its related sandboxes:

1. Navigate to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click the three-dot menu (**⋮**) next to a forked sandbox
3. Select **View Forks**

The fork tree displays each sandbox in the hierarchy along with its current state and creation time, allowing you to trace the lineage of any fork back to its origin.

## Label Sandboxes

Daytona provides methods to set sandbox labels.

Setting labels replaces the full label set for the sandbox. Include all labels you want to keep in the request. If you omit an existing label, it will be removed.

```go
err := sandbox.SetLabels(ctx, map[string]string{
	"team": "platform",
	"env":  "staging",
})
```

## Create Snapshot from Sandbox
> **Caution: Experimental**
> This feature is experimental. To request access, contact [support@daytona.io](mailto:support@daytona.io).

Daytona provides methods to create [snapshots](./snapshots.md) from sandboxes.

A snapshot captures an immutable, point-in-time copy of a sandbox's filesystem and memory that you can use as a base to create new sandboxes, effectively templating a known-good environment for reuse. You can think of it as a checkpoint you can restore from whenever you need a clean, identical starting point.

```go
// Create snapshot from sandbox
err := sandbox.ExperimentalCreateSnapshot(ctx, "my-sandbox-snapshot")
if err != nil {
    return err
}
```

## Delete Sandboxes

Daytona provides methods to delete sandboxes.

1. Navigate to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click the **Delete** button next to the sandbox you want to delete.

```go
err = sandbox.Delete(ctx)
```

## Sandbox lifecycle

A sandbox can have several different states. Each state reflects the status of your sandbox.

- [**Creating**](#create-sandboxes): the sandbox is provisioning and will be ready to use
- [**Starting**](#start-sandboxes): the sandbox is starting and will be ready to use
- [**Started**](#start-sandboxes): the sandbox has started and is ready to use
- [**Stopping**](#stop-sandboxes): the sandbox is stopping and will no longer accept requests
- [**Stopped**](#stop-sandboxes): the sandbox has stopped and is no longer running
- [**Deleting**](#delete-sandboxes): the sandbox is deleting and will be removed
- [**Deleted**](#delete-sandboxes): the sandbox has been deleted and no longer exists
- [**Archiving**](#archive-sandboxes): the sandbox is archiving and its state will be preserved
- [**Archived**](#archive-sandboxes): the sandbox has been archived and its state is preserved
- [**Resizing**](#resize-sandboxes): the sandbox is being resized to a new set of resources
- [**Error**](#recover-sandboxes): the sandbox is in an error state and needs to be recovered
- **Restoring**: the sandbox is being restored from archive and will be ready to use shortly
- **Unknown**: the default sandbox state before it is created
- **Pulling Snapshot**: the sandbox is pulling a [snapshot](./snapshots.md) to provide a base environment
- **Building Snapshot**: the sandbox is building a [snapshot](./snapshots.md) to provide a base environment
- **Build Pending**: the sandbox build is pending and will start shortly
- **Build Failed**: the sandbox build failed and needs to be retried

The diagram demonstrates the states and possible transitions between them.


## Multiple runtime support

Daytona sandboxes support Python, TypeScript, and JavaScript programming language runtimes for direct code execution inside the sandbox. The `language` parameter controls which programming language runtime is used for the sandbox:

- **`python`**
- **`typescript`**
- **`javascript`**

If omitted, the Daytona SDK will default to `python`. To override this, explicitly set the `language` value when creating the sandbox.

## Automated lifecycle management

Daytona sandboxes can be automatically stopped, archived, and deleted based on user-defined intervals. You can also refresh the last activity timestamp to explicitly signal activity when lifecycle behavior depends on inactivity windows.

### Update sandbox last activity

Daytona provides methods to update a sandbox's last activity timestamp.

This updates the sandbox's recorded activity time without changing its runtime state. It is useful when your workflow is driven by external systems or background orchestration that may not reset inactivity tracking.

For example, if you run long-lived automation around a sandbox and want to avoid unintended auto-stop behavior, call this operation periodically to indicate that the sandbox is still actively used.


### Auto-stop interval

Daytona provides methods to set the auto-stop interval.

The auto-stop interval sets the amount of time after which a running sandbox will be automatically stopped. The auto-stop triggers even if there are internal processes running in the sandbox.

The system differentiates between "internal processes" and "active user interaction". Merely having a script or background task running is not sufficient to keep the sandbox alive.

- [What resets the timer](#what-resets-the-timer)
- [What does not reset the timer](#what-does-not-reset-the-timer)

The parameter can either be set to:

- a time interval in minutes
- `0`: disables the auto-stop functionality, allowing the sandbox to run indefinitely

If the parameter is not set, the default interval of `15 minutes` will be used.

```go
// Create a sandbox with auto-stop disabled
autoStopInterval := 0
params := types.SnapshotParams{
    Snapshot: "my-snapshot-name",
    SandboxBaseParams: types.SandboxBaseParams{
        AutoStopInterval: &autoStopInterval,
    },
}
sandbox, err := client.Create(ctx, params)
```

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

Daytona provides methods to set the auto-archive interval.

The auto-archive interval sets the amount of time after which a continuously stopped sandbox will be automatically archived. The parameter can either be set to:

- a time interval in minutes
- `0`: the maximum interval of `30 days` will be used

If the parameter is not set, the default interval of `7 days` will be used.

```go
// Create a sandbox with auto-archive after 1 hour
autoArchiveInterval := 60
params := types.SnapshotParams{
    Snapshot: "my-snapshot-name",
    SandboxBaseParams: types.SandboxBaseParams{
        AutoArchiveInterval: &autoArchiveInterval,
    },
}
sandbox, err := client.Create(ctx, params)
```

### Auto-delete interval

Daytona provides methods to set the auto-delete interval.

The auto-delete interval sets the amount of time after which a continuously stopped sandbox will be automatically deleted. By default, sandboxes will never be automatically deleted. The parameter can either be set to:

- a time interval in minutes
- `-1`: disables the auto-delete functionality
- `0`: the sandbox will be deleted immediately after stopping

If the parameter is not set, the sandbox will not be deleted automatically.

```go
// Create a sandbox with auto-delete after 1 hour
autoDeleteInterval := 60
params := types.SnapshotParams{
    Snapshot: "my-snapshot-name",
    SandboxBaseParams: types.SandboxBaseParams{
        AutoDeleteInterval: &autoDeleteInterval,
    },
}
sandbox, err := client.Create(ctx, params)

// Delete the sandbox immediately after it has been stopped
zeroInterval := 0
err = sandbox.SetAutoDeleteInterval(ctx, &zeroInterval)

// Disable auto-deletion
disableInterval := -1
err = sandbox.SetAutoDeleteInterval(ctx, &disableInterval)
```

### Running indefinitely

Daytona provides methods to run sandboxes indefinitely.

By default, Daytona sandboxes auto-stop after 15 minutes of inactivity. To keep a sandbox running without interruption, set the auto-stop interval to `0` when creating a new sandbox:

```go
// Disables the auto-stop feature - default is 15 minutes
autoStopInterval := 0
params := types.SnapshotParams{
    Snapshot: "my_awesome_snapshot",
    SandboxBaseParams: types.SandboxBaseParams{
        AutoStopInterval: &autoStopInterval,
    },
}
sandbox, err := client.Create(ctx, params)
```

## See Also
- [Python SDK - sandboxes](../python-sdk/sandboxes.md)
- [TypeScript SDK - sandboxes](../typescript-sdk/sandboxes.md)
