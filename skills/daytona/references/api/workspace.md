# Workspace API


## Contents

- GET `/workspace`
- POST `/workspace`
- GET `/workspace/{workspaceId}`}
- DELETE `/workspace/{workspaceId}`}
- POST `/workspace/{workspaceId}/start`/start}
- POST `/workspace/{workspaceId}/stop`/stop}
- PUT `/workspace/{workspaceId}/labels`/labels}
- POST `/workspace/{workspaceId}/backup`/backup}
- POST `/workspace/{workspaceId}/public/{isPublic}`/public/{isPublic}}
- POST `/workspace/{workspaceId}/autostop/{interval}`/autostop/{interval}}
- POST `/workspace/{workspaceId}/autoarchive/{interval}`/autoarchive/{interval}}
- POST `/workspace/{workspaceId}/archive`/archive}
- GET `/workspace/{workspaceId}/ports/{port}/preview-url`/ports/{port}/preview-url}
- GET `/workspace/{workspaceId}/build-logs`/build-logs}

## GET `/workspace` {#daytona/tag/workspace/GET/workspace}

**[DEPRECATED] List all workspaces**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `verbose` | query | boolean | No | Include verbose output |
| `labels` | query | string | No | JSON encoded labels to filter by |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | List of all workspacees | array of Workspace |

---

## POST `/workspace` {#daytona/tag/workspace/POST/workspace}

**[DEPRECATED] Create a new workspace**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |

### Request Body

Schema: **CreateWorkspace**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | string | No | The image used for the workspace |
| `user` | string | No | The user associated with the project |
| `env` | object | No | Environment variables for the workspace |
| `labels` | object | No | Labels for the workspace |
| `public` | boolean | No | Whether the workspace http preview is publicly accessible |
| `class` | string | No | The workspace class type |
| `target` | string | No | The target (region) where the workspace will be created |
| `cpu` | integer | No | CPU cores allocated to the workspace |
| `gpu` | integer | No | GPU units allocated to the workspace |
| `memory` | integer | No | Memory allocated to the workspace in GB |
| `disk` | integer | No | Disk space allocated to the workspace in GB |
| `autoStopInterval` | integer | No | Auto-stop interval in minutes (0 means disabled) |
| `autoArchiveInterval` | integer | No | Auto-archive interval in minutes (0 means the maximum interval will be used) |
| `volumes` | array of [SandboxVolume](#schema-sandboxvolume) | No | Array of volumes to attach to the workspace |
| `buildInfo` | object | No | Build information for the workspace |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | The workspace has been successfully created. | Workspace |

---

## GET `/workspace/{workspaceId}` {#daytona/tag/workspace/GET/workspace/{workspaceId}}

**[DEPRECATED] Get workspace details**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `workspaceId` | path | string | Yes | ID of the workspace |
| `verbose` | query | boolean | No | Include verbose output |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Workspace details | Workspace |

---

## DELETE `/workspace/{workspaceId}` {#daytona/tag/workspace/DELETE/workspace/{workspaceId}}

**[DEPRECATED] Delete workspace**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `workspaceId` | path | string | Yes | ID of the workspace |
| `force` | query | boolean | Yes |  |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Workspace has been deleted |  |

---

## POST `/workspace/{workspaceId}/start` {#daytona/tag/workspace/POST/workspace/{workspaceId}/start}

**[DEPRECATED] Start workspace**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `workspaceId` | path | string | Yes | ID of the workspace |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Workspace has been started |  |

---

## POST `/workspace/{workspaceId}/stop` {#daytona/tag/workspace/POST/workspace/{workspaceId}/stop}

**[DEPRECATED] Stop workspace**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `workspaceId` | path | string | Yes | ID of the workspace |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Workspace has been stopped |  |

---

## PUT `/workspace/{workspaceId}/labels` {#daytona/tag/workspace/PUT/workspace/{workspaceId}/labels}

**[DEPRECATED] Replace workspace labels**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `workspaceId` | path | string | Yes | ID of the workspace |

### Request Body

Schema: **SandboxLabels**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `labels` | object | Yes | Key-value pairs of labels |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Labels have been successfully replaced | SandboxLabels |

---

## POST `/workspace/{workspaceId}/backup` {#daytona/tag/workspace/POST/workspace/{workspaceId}/backup}

**[DEPRECATED] Create workspace backup**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `workspaceId` | path | string | Yes | ID of the workspace |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Workspace backup has been initiated | Workspace |

---

## POST `/workspace/{workspaceId}/public/{isPublic}` {#daytona/tag/workspace/POST/workspace/{workspaceId}/public/{isPublic}}

**[DEPRECATED] Update public status**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `workspaceId` | path | string | Yes | ID of the workspace |
| `isPublic` | path | boolean | Yes | Public status to set |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 201 |  |  |

---

## POST `/workspace/{workspaceId}/autostop/{interval}` {#daytona/tag/workspace/POST/workspace/{workspaceId}/autostop/{interval}}

**[DEPRECATED] Set workspace auto-stop interval**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `workspaceId` | path | string | Yes | ID of the workspace |
| `interval` | path | number | Yes | Auto-stop interval in minutes (0 to disable) |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Auto-stop interval has been set |  |

---

## POST `/workspace/{workspaceId}/autoarchive/{interval}` {#daytona/tag/workspace/POST/workspace/{workspaceId}/autoarchive/{interval}}

**[DEPRECATED] Set workspace auto-archive interval**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `workspaceId` | path | string | Yes | ID of the workspace |
| `interval` | path | number | Yes | Auto-archive interval in minutes (0 means the maximum interval will be used) |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Auto-archive interval has been set |  |

---

## POST `/workspace/{workspaceId}/archive` {#daytona/tag/workspace/POST/workspace/{workspaceId}/archive}

**[DEPRECATED] Archive workspace**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `workspaceId` | path | string | Yes |  |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Workspace has been archived |  |

---

## GET `/workspace/{workspaceId}/ports/{port}/preview-url` {#daytona/tag/workspace/GET/workspace/{workspaceId}/ports/{port}/preview-url}

**[DEPRECATED] Get preview URL for a workspace port**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `workspaceId` | path | string | Yes | ID of the workspace |
| `port` | path | number | Yes | Port number to get preview URL for |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Preview URL for the specified port | WorkspacePortPreviewUrl |

---

## GET `/workspace/{workspaceId}/build-logs` {#daytona/tag/workspace/GET/workspace/{workspaceId}/build-logs}

**[DEPRECATED] Get build logs**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `workspaceId` | path | string | Yes | ID of the workspace |
| `follow` | query | boolean | No | Whether to follow the logs stream |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Build logs stream |  |

---
