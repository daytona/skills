# Process API


## Contents

- POST `/process/code-run`
- POST `/process/execute`
- GET `/process/pty`
- POST `/process/pty`
- GET `/process/pty/{sessionId}`}
- DELETE `/process/pty/{sessionId}`}
- GET `/process/pty/{sessionId}/connect`/connect}
- POST `/process/pty/{sessionId}/resize`/resize}
- GET `/process/session`
- POST `/process/session`
- GET `/process/session/entrypoint`
- GET `/process/session/entrypoint/logs`
- GET `/process/session/{sessionId}`}
- DELETE `/process/session/{sessionId}`}
- GET `/process/session/{sessionId}/command/{commandId}`/command/{commandId}}
- POST `/process/session/{sessionId}/command/{commandId}/input`/command/{commandId}/input}
- GET `/process/session/{sessionId}/command/{commandId}/logs`/command/{commandId}/logs}
- POST `/process/session/{sessionId}/exec`/exec}

## POST `/process/code-run` {#daytona-toolbox/tag/process/POST/process/code-run}

**Execute code**

Execute Python, JavaScript, or TypeScript code and return output, exit code, and artifacts

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Code execution request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/process/execute` {#daytona-toolbox/tag/process/POST/process/execute}

**Execute a command**

Execute a shell command and return the output and exit code

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Command execution request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## GET `/process/pty` {#daytona-toolbox/tag/process/GET/process/pty}

**List all PTY sessions**

Get a list of all active pseudo-terminal sessions

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/process/pty` {#daytona-toolbox/tag/process/POST/process/pty}

**Create a new PTY session**

Create a new pseudo-terminal session with specified configuration

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | PTY session creation request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 201 | Created |  |

---

## GET `/process/pty/{sessionId}` {#daytona-toolbox/tag/process/GET/process/pty/{sessionId}}

**Get PTY session information**

Get detailed information about a specific pseudo-terminal session

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `sessionId` | path | string | Yes | PTY session ID |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## DELETE `/process/pty/{sessionId}` {#daytona-toolbox/tag/process/DELETE/process/pty/{sessionId}}

**Delete a PTY session**

Delete a pseudo-terminal session and terminate its process

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `sessionId` | path | string | Yes | PTY session ID |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## GET `/process/pty/{sessionId}/connect` {#daytona-toolbox/tag/process/GET/process/pty/{sessionId}/connect}

**Connect to PTY session via WebSocket**

Establish a WebSocket connection to interact with a pseudo-terminal session

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `sessionId` | path | string | Yes | PTY session ID |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 101 | Switching Protocols - WebSocket connection established |  |

---

## POST `/process/pty/{sessionId}/resize` {#daytona-toolbox/tag/process/POST/process/pty/{sessionId}/resize}

**Resize a PTY session**

Resize the terminal dimensions of a pseudo-terminal session

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `sessionId` | path | string | Yes | PTY session ID |
| `request` | body | string | Yes | Resize request with new dimensions |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## GET `/process/session` {#daytona-toolbox/tag/process/GET/process/session}

**List all sessions**

Get a list of all active shell sessions

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/process/session` {#daytona-toolbox/tag/process/POST/process/session}

**Create a new session**

Create a new shell session for command execution

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Session creation request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 201 | Created |  |

---

## GET `/process/session/entrypoint` {#daytona-toolbox/tag/process/GET/process/session/entrypoint}

**Get entrypoint session details**

Get details of an entrypoint session including its commands

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## GET `/process/session/entrypoint/logs` {#daytona-toolbox/tag/process/GET/process/session/entrypoint/logs}

**Get entrypoint logs**

Get logs for a sandbox entrypoint session. Returns JSON with separated stdout/stderr for SDK >= 0.161.0, plain text otherwise. Supports WebSocket streaming.

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `follow` | query | string | No | Follow logs in real-time (WebSocket only) |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Entrypoint log content |  |

---

## GET `/process/session/{sessionId}` {#daytona-toolbox/tag/process/GET/process/session/{sessionId}}

**Get session details**

Get details of a specific session including its commands

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `sessionId` | path | string | Yes | Session ID |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## DELETE `/process/session/{sessionId}` {#daytona-toolbox/tag/process/DELETE/process/session/{sessionId}}

**Delete a session**

Delete an existing shell session

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `sessionId` | path | string | Yes | Session ID |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 204 | No Content |  |

---

## GET `/process/session/{sessionId}/command/{commandId}` {#daytona-toolbox/tag/process/GET/process/session/{sessionId}/command/{commandId}}

**Get session command details**

Get details of a specific command within a session

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `sessionId` | path | string | Yes | Session ID |
| `commandId` | path | string | Yes | Command ID |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/process/session/{sessionId}/command/{commandId}/input` {#daytona-toolbox/tag/process/POST/process/session/{sessionId}/command/{commandId}/input}

**Send input to command**

Send input data to a running command in a session for interactive execution

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `sessionId` | path | string | Yes | Session ID |
| `commandId` | path | string | Yes | Command ID |
| `request` | body | string | Yes | Input send request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 204 | No Content |  |

---

## GET `/process/session/{sessionId}/command/{commandId}/logs` {#daytona-toolbox/tag/process/GET/process/session/{sessionId}/command/{commandId}/logs}

**Get session command logs**

Get logs for a specific command within a session. Returns JSON with separated stdout/stderr for SDK >= 0.167.0, plain text otherwise. Supports WebSocket streaming.

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `sessionId` | path | string | Yes | Session ID |
| `commandId` | path | string | Yes | Command ID |
| `follow` | query | string | No | Follow logs in real-time (WebSocket only) |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Log content (JSON for new SDKs, plain text for old SDKs) |  |

---

## POST `/process/session/{sessionId}/exec` {#daytona-toolbox/tag/process/POST/process/session/{sessionId}/exec}

**Execute command in session**

Execute a command within an existing shell session

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `sessionId` | path | string | Yes | Session ID |
| `request` | body | string | Yes | Command execution request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |
| 202 | Accepted |  |

---
