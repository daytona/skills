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

```java
import io.daytona.sdk.Daytona;
import io.daytona.sdk.Sandbox;
import io.daytona.sdk.model.SessionExecuteRequest;
import io.daytona.sdk.model.SessionExecuteResponse;

public class App {
    public static void main(String[] args) throws InterruptedException {
        try (Daytona daytona = new Daytona()) {
            Sandbox sandbox = daytona.create();
            String sessionId = "streaming-session";
            sandbox.getProcess().createSession(sessionId);

            SessionExecuteResponse command = sandbox.getProcess().executeSessionCommand(
                    sessionId,
                    new SessionExecuteRequest(
                            "for i in {1..5}; do echo \"Step $i\"; echo \"Error $i\" >&2; sleep 1; done",
                            true));

            Thread logThread = new Thread(() -> sandbox.getProcess().getSessionCommandLogs(
                    sessionId,
                    command.getCmdId(),
                    stdout -> System.out.print("[STDOUT]: " + stdout),
                    stderr -> System.err.print("[STDERR]: " + stderr)));
            logThread.start();

            System.out.println("Continuing execution while logs are streaming...");
            Thread.sleep(3000);
            System.out.println("Other operations completed!");

            logThread.join();

            sandbox.delete();
        }
    }
}
```

## Retrieve all existing logs

If the command has a predictable duration, or if you don't need to run it in the background but want to
periodically check all existing logs, you can use the following example to get the logs up to the current point in time.

```java
import io.daytona.sdk.Daytona;
import io.daytona.sdk.Sandbox;
import io.daytona.sdk.model.SessionCommandLogsResponse;
import io.daytona.sdk.model.SessionExecuteRequest;
import io.daytona.sdk.model.SessionExecuteResponse;

public class App {
    public static void main(String[] args) throws InterruptedException {
        try (Daytona daytona = new Daytona()) {
            Sandbox sandbox = daytona.create();
            String sessionId = "exec-session-1";
            sandbox.getProcess().createSession(sessionId);

            SessionExecuteResponse command = sandbox.getProcess().executeSessionCommand(
                    sessionId,
                    new SessionExecuteRequest(
                            "echo 'Hello from stdout' && echo 'Hello from stderr' >&2",
                            false));
            System.out.println("[STDOUT]: " + command.getStdout());
            System.out.println("[STDERR]: " + command.getStderr());
            System.out.println("[OUTPUT]: " + command.getOutput());

            SessionExecuteResponse asyncCmd = sandbox.getProcess().executeSessionCommand(
                    sessionId,
                    new SessionExecuteRequest(
                            "while true; do if (( RANDOM % 2 )); then echo \"All good at $(date)\"; else echo \"Oops, an error at $(date)\" >&2; fi; sleep 1; done",
                            true));
            Thread.sleep(5000);
            SessionCommandLogsResponse logs = sandbox.getProcess().getSessionCommandLogs(sessionId, asyncCmd.getCmdId());
            System.out.println("[STDOUT]: " + logs.getStdout());
            System.out.println("[STDERR]: " + logs.getStderr());
            System.out.println("[OUTPUT]: " + logs.getOutput());

            sandbox.delete();
        }
    }
}
```

## See Also
- [Python SDK - log-streaming](../python-sdk/log-streaming.md)
- [TypeScript SDK - log-streaming](../typescript-sdk/log-streaming.md)
