## Contents

- Stream logs with callbacks
- Retrieve all existing logs
- See Also




Log streaming allows you to access and process logs as they are being produced, while the process is still running. When executing long-running processes in a sandbox, you often want to access and process their logs in **real-time**.

Real-time streaming is especially useful for **debugging**, **monitoring**, or integrating with **observability tools**.

- [**Log streaming**](#stream-logs-with-callbacks): stream logs as they are being produced, while the process is still running.
- [**Fetching log snapshot**](#retrieve-all-existing-logs): retrieve all logs up to a certain point.

This guide covers how to use log streaming with callbacks and fetching log snapshots in both asynchronous and synchronous modes.

For entrypoint log streaming, see [Process & Code Execution](./process-code-execution.md#entrypoint-session). To stream logs while sending input to a running command, see [Execute interactive commands](./process-code-execution.md#execute-interactive-commands).

## Stream logs with callbacks

If your sandboxed process is part of a larger system and is expected to run for an extended period (or indefinitely),
you can process logs asynchronously **in the background**, while the rest of your system continues executing.

This is ideal for:

- Continuous monitoring
- Debugging long-running jobs
- Live log forwarding or visualizations
> **Tip: Python callbacks**
> When streaming with the Python SDK, avoid blocking operations inside stdout/stderr callbacks. Blocking synchronous callbacks can cause WebSocket disconnections. Use async callbacks where possible.

```typescript
import { Daytona, SessionExecuteRequest } from '@daytona/sdk'

async function main() {
  const daytona = new Daytona()
  const sandbox = await daytona.create()
  const sessionId = "exec-session-1"
  await sandbox.process.createSession(sessionId)

  const command = await sandbox.process.executeSessionCommand(
    sessionId,
    {
      command: 'for i in {1..5}; do echo "Step $i"; echo "Error $i" >&2; sleep 1; done',
      runAsync: true,
    },
  )

  // Stream logs with separate callbacks
  const logsTask = sandbox.process.getSessionCommandLogs(
    sessionId,
    command.cmdId!,
    (stdout) => console.log('[STDOUT]:', stdout),
    (stderr) => console.log('[STDERR]:', stderr),
  )

  console.log('Continuing execution while logs are streaming...')
  await new Promise((resolve) => setTimeout(resolve, 3000))
  console.log('Other operations completed!')

  // Wait for the logs to complete
  await logsTask

  await sandbox.delete()
}

main()
```

## Retrieve all existing logs

If the command has a predictable duration, or if you don't need to run it in the background but want to
periodically check all existing logs, you can use the following example to get the logs up to the current point in time.

```typescript
import { Daytona, SessionExecuteRequest } from '@daytona/sdk'

async function main() {
  const daytona = new Daytona()
  const sandbox = await daytona.create()
  const sessionId = "exec-session-1"
  await sandbox.process.createSession(sessionId)

  // Execute a blocking command and wait for the result
  const command = await sandbox.process.executeSessionCommand(
    sessionId,
    {
      command: 'echo "Hello from stdout" && echo "Hello from stderr" >&2',
    },
  )
  console.log(`[STDOUT]: ${command.stdout}`)
  console.log(`[STDERR]: ${command.stderr}`)
  console.log(`[OUTPUT]: ${command.output}`)

  // Or execute command in the background and get the logs later
  const command2 = await sandbox.process.executeSessionCommand(
    sessionId,
    {
      command: 'while true; do if (( RANDOM % 2 )); then echo "All good at $(date)"; else echo "Oops, an error at $(date)" >&2; fi; sleep 1; done',
      runAsync: true,
    },
  )
  await new Promise((resolve) => setTimeout(resolve, 5000))
  // Get the logs up to the current point in time
  const logs = await sandbox.process.getSessionCommandLogs(sessionId, command2.cmdId!)
  console.log(`[STDOUT]: ${logs.stdout}`)
  console.log(`[STDERR]: ${logs.stderr}`)
  console.log(`[OUTPUT]: ${logs.output}`)

  await sandbox.delete()
}

main()
```

## See Also
- [Python SDK - log-streaming](../python-sdk/log-streaming.md)
