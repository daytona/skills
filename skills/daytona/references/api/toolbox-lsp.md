# Lsp API


## Contents

- POST `/lsp/completions`
- POST `/lsp/did-close`
- POST `/lsp/did-open`
- GET `/lsp/document-symbols`
- POST `/lsp/start`
- POST `/lsp/stop`
- GET `/lsp/workspacesymbols`

## POST `/lsp/completions` {#daytona-toolbox/tag/lsp/POST/lsp/completions}

**Get code completions**

Get code completion suggestions from the LSP server

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Completion request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/lsp/did-close` {#daytona-toolbox/tag/lsp/POST/lsp/did-close}

**Notify document closed**

Notify the LSP server that a document has been closed

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Document request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/lsp/did-open` {#daytona-toolbox/tag/lsp/POST/lsp/did-open}

**Notify document opened**

Notify the LSP server that a document has been opened

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Document request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## GET `/lsp/document-symbols` {#daytona-toolbox/tag/lsp/GET/lsp/document-symbols}

**Get document symbols**

Get symbols (functions, classes, etc.) from a document

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `languageId` | query | string | Yes | Language ID (e.g., python, typescript) |
| `pathToProject` | query | string | Yes | Path to project |
| `uri` | query | string | Yes | Document URI |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/lsp/start` {#daytona-toolbox/tag/lsp/POST/lsp/start}

**Start LSP server**

Start a Language Server Protocol server for the specified language

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | LSP server request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/lsp/stop` {#daytona-toolbox/tag/lsp/POST/lsp/stop}

**Stop LSP server**

Stop a Language Server Protocol server

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | LSP server request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## GET `/lsp/workspacesymbols` {#daytona-toolbox/tag/lsp/GET/lsp/workspacesymbols}

**Get workspace symbols**

Search for symbols across the entire workspace

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `query` | query | string | Yes | Search query |
| `languageId` | query | string | Yes | Language ID (e.g., python, typescript) |
| `pathToProject` | query | string | Yes | Path to project |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---
