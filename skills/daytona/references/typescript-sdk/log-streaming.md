
Log streaming allows you to access and process logs as they are being produced, while the process is still running. When executing long-running processes in a sandbox, you often want to access and process their logs in **real-time**.

Real-time streaming is especially useful for **debugging**, **monitoring**, or integrating with **observability tools**.

- [**Log streaming**](#stream-logs-with-callbacks): stream logs as they are being produced, while the process is still running.
- [**Fetching log snapshot**](#retrieve-all-existing-logs): retrieve all logs up to a certain point.

This guide covers how to use log streaming with callbacks and fetching log snapshots in both asynchronous and synchronous modes.
> **Note:**
> Starting with version `0.27.0`, you can retrieve session command logs in two distinct streams: **stdout** and **stderr**.

## Stream logs with callbacks

If your sandboxed process is part of a larger system and is expected to run for an extended period (or indefinitely),
you can process logs asynchronously **in the background**, while the rest of your system continues executing.

This is ideal for:

- Continuous monitoring
- Debugging long-running jobs
- Live log forwarding or visualizations


For more information, see the [Python SDK](../python-sdk/sync/process.md), [TypeScript SDK](./process.md), [Ruby SDK](../ruby-sdk/process.md), [Go SDK](../go-sdk/README.md), and [API](../api/README.md#daytona-toolbox/tag/process) references.

> [**get_session_command_logs_async (Python SDK)**](../python-sdk/sync/process.md#processget_session_command_logs_async)
>
> [**getSessionCommandLogs (TypeScript SDK)**](./process.md#getsessioncommandlogs)
>
> [**get_session_command_logs_async (Ruby SDK)**](../ruby-sdk/process.md#get_session_command_logs_async)
>
> [**GetSessionCommandLogsStream (Go SDK)**](../go-sdk/daytona.md#ProcessService.GetSessionCommandLogsStream)
>
> [**get session command logs (API)**](../api/README.md#daytona-toolbox/tag/process/POST/process/session/{sessionId}/exec)

## Retrieve all existing logs

If the command has a predictable duration, or if you don't need to run it in the background but want to
periodically check all existing logs, you can use the following example to get the logs up to the current point in time.


For more information, see the [Python SDK](../python-sdk/sync/process.md), [TypeScript SDK](./process.md), [Ruby SDK](../ruby-sdk/process.md), [Go SDK](../go-sdk/README.md), and [API](../api/README.md#daytona-toolbox/tag/process) references.

> [**get_session_command_logs (Python SDK)**](../python-sdk/sync/process.md#processget_session_command_logs)
>
> [**getSessionCommandLogs (TypeScript SDK)**](./process.md#getsessioncommandlogs)
>
> [**get_session_command_logs (Ruby SDK)**](../ruby-sdk/process.md#get_session_command_logs)
>
> [**GetSessionCommandLogs (Go SDK)**](../go-sdk/daytona.md#ProcessService.GetSessionCommandLogs)
>
> [**get session command logs (API)**](../api/README.md#daytona-toolbox/tag/process/POST/process/session/{sessionId}/exec)

## See Also
- [Python SDK - log-streaming](../python-sdk/log-streaming.md)
