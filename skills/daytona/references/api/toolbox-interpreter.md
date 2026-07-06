# Interpreter API

## GET `/process/interpreter/context` {#daytona-toolbox/tag/interpreter/GET/process/interpreter/context}

**List all user-created interpreter contexts**

Returns information about all user-created interpreter contexts (excludes default context)

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/process/interpreter/context` {#daytona-toolbox/tag/interpreter/POST/process/interpreter/context}

**Create a new interpreter context**

Creates a new isolated interpreter context with optional working directory and language

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Context configuration |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |
| 400 | Bad Request |  |
| 500 | Internal Server Error |  |

---

## DELETE `/process/interpreter/context/{id}` {#daytona-toolbox/tag/interpreter/DELETE/process/interpreter/context/{id}}

**Delete an interpreter context**

Deletes an interpreter context and shuts down its worker process

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `id` | path | string | Yes | Context ID |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |
| 400 | Bad Request |  |
| 404 | Not Found |  |

---

## GET `/process/interpreter/execute` {#daytona-toolbox/tag/interpreter/GET/process/interpreter/execute}

**Execute code in an interpreter context**

Executes code in a specified context (or default context if not specified) via WebSocket streaming

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 101 | Switching Protocols |  |

---
