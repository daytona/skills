## Contents

- Sandbox lifecycle
- Multiple runtime support
- Create Sandboxes
- Start Sandboxes
- List Sandboxes
- Stop Sandboxes
- Archive Sandboxes
- Recover Sandboxes
- Resize Sandboxes
- Delete Sandboxes
- Automated lifecycle management
- See Also




Daytona provides **full composable computers** — **sandboxes** — for AI agents. Sandboxes are isolated runtime environments you can manage programmatically to run code. Each sandbox runs in isolation, giving it a dedicated kernel, filesystem, network stack, and allocated vCPU, RAM, and disk. Agents get access to a full composable computer environment where they can install packages, run servers, compile code, and manage processes.

Sandboxes have **1 vCPU**, **1GB RAM**, and **3GiB disk** by default. [Organizations](../platform/organizations.md) get a maximum sandbox resource limit of **4 vCPUs**, **8GB RAM**, and **10GB disk**. For more power, see [resources](#resources) or contact [support@daytona.io](mailto:support@daytona.io).

Sandboxes use [snapshots](./snapshots.md) to capture a fully configured environment (base OS, installed packages, dependencies, and configuration) to create new sandboxes.

Each sandbox has its own network stack with per-sandbox firewall rules. By default, sandboxes follow standard network policies, but you can restrict egress to a specific set of allowed destinations or block all outbound traffic entirely. For details on configuring network access, see [network limits](./network-limits.md).

A detailed overview of the Daytona platform is available in the [architecture](https://www.daytona.io/docs/en/architecture) section.

## Sandbox lifecycle

Throughout its lifecycle, a sandbox can have several different states. Each state reflects the current status of your sandbox:

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

To view or update the current state of a sandbox, navigate to the [sandbox details page](#sandbox-details-page) or access the sandbox `state` attribute using the [SDKs](./getting-started.md#sdks), [API](../api/README.md#daytona/tag/sandbox/GET/sandbox/{sandboxIdOrName}), or [CLI](../cli.md#daytona-info).

The diagram below demonstrates the states and possible transitions between them.


## Multiple runtime support

Daytona sandboxes support Python, TypeScript, and JavaScript programming language runtimes for direct code execution inside the sandbox. The `language` parameter controls which programming language runtime is used for the sandbox:

- **`python`**
- **`typescript`**
- **`javascript`**

If omitted, the Daytona SDK will default to `python`. To override this, explicitly set the `language` value when creating the sandbox.

## Create Sandboxes

Daytona provides methods to create sandboxes using the [Daytona Dashboard ↗](https://app.daytona.io/dashboard/) or programmatically using the Daytona [Python](../python-sdk/sync/sandbox.md), [TypeScript](./sandbox.md), [Ruby](../ruby-sdk/sandbox.md), [Go](../go-sdk/daytona.md#type-sandbox) **SDKs**, [CLI](../cli.md#daytona-create), or [API](../api/README.md#daytona/tag/sandbox).

You can specify [programming language runtime](./sandboxes.md#multiple-runtime-support), [snapshots](./snapshots.md), [resources](./sandboxes.md#resources), [regions](./regions.md), [environment variables](./configuration.md#environment-variables), and [volumes](./volumes.md) for each sandbox. Running sandboxes utilize CPU, memory, and disk storage. Every resource is charged per second of usage.

1. Navigate to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click the **Create Sandbox** button
3. Enter the name of the sandbox (optional)
4. Select a source for the sandbox (optional):

- [Snapshot](./snapshots.md): a pre-configured sandbox template
- **Image**: OCI-compliant container image ([public](./snapshots.md#using-public-images), [local](./snapshots.md#using-local-images), [private registries](./snapshots.md#using-images-from-private-registries)). Images require setting [sandbox resources](./sandboxes.md#resources). Default: **1 vCPU**, **1GB RAM**, **3GiB disk**.

5. Select a [region](./regions.md) (optional): if not specified, your organization's default region will be used
6. Define [sandbox lifecycle management](#automated-lifecycle-management) options (optional) or set as an [ephemeral sandbox](#ephemeral-sandboxes)
7. Add environment variables in key-value pairs or import them from a **`.env`** file (optional)
8. Add labels in key-value pairs (optional)
9. Select network settings (optional):

- **Public HTTP preview**: allow public access to HTTP [preview URLs](./preview.md)
- **Block all network access**: block all outbound network access

10. Click the **Create** button to create a sandbox

```typescript
import { Daytona } from '@daytona/sdk';

const daytona = new Daytona();

// Create a sandbox
const sandbox = await daytona.create();

// Create a sandbox with typescript
const sandbox = await daytona.create({ language: 'typescript' });

// Create a sandbox with a custom name
const sandbox = await daytona.create({ name: 'my_awesome_sandbox' });

// Create a sandbox with custom labels
const sandbox = await daytona.create({ labels: { LABEL: 'label' } });
```

### Resources

Sandboxes have **1 vCPU**, **1GB RAM**, and **3GiB disk** by default. Organizations get a maximum sandbox resource limit of **4 vCPUs**, **8GB RAM**, and **10GB disk**.

To set custom sandbox resources (CPU, memory, and disk space), use the `Resources` class:

```typescript
import { Daytona, Image } from "@daytona/sdk";

async function main() {
  const daytona = new Daytona();

  // Create a sandbox with custom resources
  const sandbox = await daytona.create({
    image: Image.debianSlim("3.12"),
    resources: {
      cpu: 2,     // 2 CPU cores
      memory: 4,  // 4GB RAM
      disk: 8,    // 8GB disk space
    },
  });
}

main();
```

All resource parameters are optional and must be integers. If not specified, Daytona will use the default values listed below.

| **Resource** | **Unit** | **Default** | **Minimum** | **Maximum** |
| ------------ | -------- | ----------- | ----------- | ----------- |
| CPU          | vCPU     | **`1`**     | **`1`**     | **`4`**     |
| Memory       | GiB      | **`1`**     | **`1`**     | **`8`**     |
| Disk         | GiB      | **`3`**     | **`1`**     | **`10`**    |

Maximum values are per-sandbox limits set at the [organization](../platform/organizations.md) level. Contact [support@daytona.io](mailto:support@daytona.io) to increase limits.

### Ephemeral Sandboxes

Ephemeral Sandboxes are automatically deleted once they are stopped. They are useful for short-lived tasks or for testing purposes.

To create an ephemeral Sandbox, set the `ephemeral` parameter to `True` when creating a sandbox:

```typescript
import { Daytona } from '@daytona/sdk';

const daytona = new Daytona();

// Create an ephemeral sandbox
const sandbox = await daytona.create({
  ephemeral: true,
  autoStopInterval: 5 // The ephemeral sandbox will be deleted after 5 minutes of inactivity
});
```
> **Note:**
> Setting ["autoDeleteInterval: 0"](#auto-delete-interval) has the same effect as setting "ephemeral" to `true`.

### Network settings (Firewall)

Daytona Sandboxes provide configurable network firewall controls to enhance security and manage connectivity.
By default, network access follows standard security policies, but you can [customize network settings](./network-limits.md) when creating a sandbox.

## Start Sandboxes

Daytona provides options to start sandboxes in [Daytona Dashboard ↗](https://app.daytona.io/dashboard/) or programmatically using the [Python SDK](../python-sdk/README.md), [TypeScript SDK](./README.md), [Ruby SDK](../ruby-sdk/README.md), [CLI](../cli.md), and [API](../api/README.md#daytona/) references.

1. Navigate to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click the start icon (**▶**) next to the sandbox you want to start.

```text
Starting sandbox with ID: <sandbox-id>
```

```typescript
const sandbox = await daytona.create({ language: 'typescript' });
// Start Sandbox
await sandbox.start();
```

## List Sandboxes

Daytona provides options to view information about sandboxes in [Daytona Dashboard ↗](https://app.daytona.io/dashboard/) via the [sandbox details page](#sandbox-details-page) or programmatically using the [Python SDK](../python-sdk/README.md), [TypeScript SDK](./README.md), [Ruby SDK](../ruby-sdk/README.md), [Go SDK](../go-sdk/daytona.md), [CLI](../cli.md), and [API](../api/README.md#daytona) references.

```typescript
// List all sandboxes
const result = await daytona.list();

// Iterate through results
for (const sandbox of result.items) {
    console.log(`Sandbox: ${sandbox.id} (state: ${sandbox.state})`);
}

// List sandboxes with labels filter
const filtered = await daytona.list({ 'env': 'dev' });
```

### Sandbox details page

[Daytona Dashboard ↗](https://app.daytona.io/dashboard/) provides a sandbox details page to view detailed information about a sandbox and interact with it directly.

1. Navigate to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click on a sandbox to open its details page

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
- [**VNC**](./vnc-access.md): a graphical desktop session for sandboxes that have a desktop environment
- [**Logs**](https://www.daytona.io/docs/en/experimental/otel-collection): a detailed record of user and system activity for the sandbox
- **Metrics**: sandbox metrics data displayed as charts
- **Traces**: distributed traces and spans collected from the sandbox
- **Spending**: usage and cost over time

## Stop Sandboxes

Daytona provides methods to stop sandboxes in [Daytona Dashboard ↗](https://app.daytona.io/dashboard/) or programmatically using the [Python SDK](../python-sdk/README.md), [TypeScript SDK](./README.md), and [Ruby SDK](../ruby-sdk/README.md).

1. Navigate to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click the stop icon (**⏹**) next to the sandbox you want to stop.

```text
Stopping sandbox with ID: <sandbox-id>
```

Stopped sandboxes maintain filesystem persistence while their memory state is cleared. They incur only disk usage costs and can be started again when needed.

The stopped state should be used when a sandbox is expected to be started again soon. Otherwise, it is recommended to stop and then archive the sandbox to eliminate disk usage costs.

```typescript
const sandbox = await daytona.create({ language: 'typescript' });

// Stop sandbox
await sandbox.stop();

console.log(sandbox.id) // 7cd11133-96c1-4cc8-9baa-c757b8f8c916

// The sandbox ID can later be used to get the sandbox and start it
const found = await daytona.get('7cd11133-96c1-4cc8-9baa-c757b8f8c916');

// Start sandbox
await found.start();
```

If you need a faster shutdown, use force stop (`force=true` / `--force`) to terminate it immediately. Force stop is ungraceful and should be used when quick termination is more important than process cleanup.

Common use cases for force stop include:

- you need to reduce stop time and can accept immediate termination
- the entrypoint ignores termination signals or hangs during shutdown

Avoid force stop for normal shutdowns where the process should flush buffers, write final state, or run cleanup hooks.

## Archive Sandboxes

Daytona provides methods to archive sandboxes in [Daytona Dashboard ↗](https://app.daytona.io/dashboard/) or programmatically using the [Python SDK](../python-sdk/README.md), [TypeScript SDK](./README.md), and [Ruby SDK](../ruby-sdk/README.md).

When sandboxes are archived, the entire filesystem state is moved to a cost-effective object storage, making it possible to keep sandboxes available for an extended period.
Starting an archived sandbox takes more time than starting a stopped sandbox, depending on its size.

A sandbox must be stopped before it can be archived and can be started again in the same way as a stopped sandbox.

```typescript
// Archive Sandbox
await sandbox.archive();
```

## Recover Sandboxes

Daytona provides methods to recover sandboxes in [Daytona Dashboard ↗](https://app.daytona.io/dashboard/) or programmatically using the [Python SDK](../python-sdk/README.md), [TypeScript SDK](./README.md), and [Ruby SDK](../ruby-sdk/README.md).

```typescript
// Recover sandbox
await sandbox.recover();
```

### Recover from error state

When a sandbox enters an error state, it can sometimes be recovered using the `recover` method, depending on the underlying error reason. The `recoverable` flag indicates whether the error state can be resolved through an automated recovery procedure.
> **Note:**
> Recovery actions are not performed automatically because they address errors that require **further user intervention**, such as freeing up storage space.

```typescript
// Check if the Sandbox is recoverable
if (sandbox.recoverable) {
    await sandbox.recover();
    console.log('Sandbox recovered successfully');
}
```

## Resize Sandboxes
> **Caution: Experimental**
> This feature is experimental. To request access, contact [support@daytona.io](mailto:support@daytona.io).

Daytona provides methods to resize [sandbox resources](#resources) after creation. On a running sandbox, you can increase CPU and memory without interruption. To decrease CPU or memory, or to increase disk capacity, stop the sandbox first. Disk size can only be increased and cannot be decreased.

```typescript
import { Daytona } from '@daytona/sdk';

const daytona = new Daytona();
const sandbox = await daytona.create();

// Resize a started sandbox (CPU and memory can be increased)
await sandbox.resize({ cpu: 2, memory: 4 });

// Resize a stopped sandbox (CPU and memory can change, disk can only increase)
await sandbox.stop();
await sandbox.resize({ cpu: 4, memory: 8, disk: 20 });
await sandbox.start();
```

## Delete Sandboxes

Daytona provides methods to delete sandboxes in [Daytona Dashboard ↗](https://app.daytona.io/dashboard/) or programmatically using the [Python SDK](../python-sdk/README.md), [TypeScript SDK](./README.md), and [Ruby SDK](../ruby-sdk/README.md).

1. Navigate to [Daytona Sandboxes ↗](https://app.daytona.io/dashboard/sandboxes)
2. Click the **Delete** button next to the sandbox you want to delete.

```text
Deleting sandbox with ID: <sandbox-id>
```

```typescript
// Delete sandbox
await sandbox.delete();
```

## Automated lifecycle management

Daytona Sandboxes can be automatically stopped, archived, and deleted based on user-defined intervals.

### Auto-stop interval

The auto-stop interval parameter sets the amount of time after which a running sandbox will be automatically stopped.

The auto-stop interval triggers even if there are internal processes running in the sandbox. The system differentiates between "internal processes" and "active user interaction". Merely having a script or background task running is not sufficient to keep the sandbox alive.

- [What resets the timer](#what-resets-the-timer)
- [What does not reset the timer](#what-does-not-reset-the-timer)

The parameter can either be set to:

- a time interval in minutes
- `0`: disables the auto-stop functionality, allowing the sandbox to run indefinitely

If the parameter is not set, the default interval of `15 minutes` will be used.

```typescript
const sandbox = await daytona.create({
    snapshot: "my-snapshot-name",
      // Disables the auto-stop feature - default is 15 minutes
    autoStopInterval: 0,
});
```

#### What resets the timer

The inactivity timer resets only for specific external interactions:

- Updates to [sandbox lifecycle states](#sandbox-lifecycle)
- Network requests through [sandbox previews](./preview.md)
- Active [SSH connections](./ssh-access.md)
- API requests to the [Daytona Toolbox SDK](../api/README.md#daytona-toolbox)

#### What does not reset the timer

The following do not reset the timer:

- SDK requests that are not toolbox actions
- Background scripts (e.g., `npm run dev` run as a fire-and-forget command)
- Long-running tasks without external interaction
- Processes that don't involve active monitoring

If you run a long-running task like LLM inference that takes more than 15 minutes to complete without any external interaction, the sandbox may auto-stop mid-process because the process itself doesn't count as "activity", therefore the timer is not reset.

### Auto-archive interval

Daytona provides methods to set the auto-archive interval using the [Python SDK](../python-sdk/README.md), [TypeScript SDK](./README.md), and [Ruby SDK](../ruby-sdk/README.md).

The auto-archive interval parameter sets the amount of time after which a continuously stopped sandbox will be automatically archived.

The parameter can either be set to:

- a time interval in minutes
- `0`: the maximum interval of `30 days` will be used

If the parameter is not set, the default interval of `7 days` will be used.

```typescript
const sandbox = await daytona.create({
    snapshot: "my-snapshot-name",
    // Auto-archive after a sandbox has been stopped for 1 hour
    autoArchiveInterval: 60,
});
```

### Auto-delete interval

Daytona provides methods to set the auto-delete interval using the [Python SDK](../python-sdk/README.md), [TypeScript SDK](./README.md), and [Ruby SDK](../ruby-sdk/README.md).

The auto-delete interval parameter sets the amount of time after which a continuously stopped sandbox will be automatically deleted. By default, sandboxes will never be automatically deleted.

The parameter can either be set to:

- a time interval in minutes
- `-1`: disables the auto-delete functionality
- `0`: the sandbox will be deleted immediately after stopping

If the parameter is not set, the sandbox will not be deleted automatically.

```typescript
const sandbox = await daytona.create({
    snapshot: "my-snapshot-name",
    // Auto-delete after a sandbox has been stopped for 1 hour
    autoDeleteInterval: 60,
});

// Delete the sandbox immediately after it has been stopped
await sandbox.setAutoDeleteInterval(0)

// Disable auto-deletion
await sandbox.setAutoDeleteInterval(-1)
```

### Running indefinitely

Daytona provides methods to run sandboxes indefinitely using the [Python SDK](../python-sdk/README.md), [TypeScript SDK](./README.md), and [Ruby SDK](../ruby-sdk/README.md).

By default, Daytona Sandboxes auto-stop after 15 minutes of inactivity. To keep a sandbox running without interruption, set the auto-stop interval to `0` when creating a new sandbox:

```typescript
const sandbox = await daytona.create({
    snapshot: "my_awesome_snapshot",
    // Disables the auto-stop feature - default is 15 minutes
    autoStopInterval: 0,
});
```

## See Also
- [TypeScript SDK - README](./README.md)
- [TypeScript SDK - daytona#resources](./daytona.md#resources)
- [TypeScript SDK - sandbox](./sandbox.md)
- [TypeScript SDK - sandbox#resize](./sandbox.md#resize)
- [Python SDK - sandboxes](../python-sdk/sandboxes.md)
