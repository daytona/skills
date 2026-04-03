# Snapshots API

## GET `/snapshots` {#daytona/tag/snapshots/GET/snapshots}

**List all snapshots**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `page` | query | number | No | Page number of the results |
| `limit` | query | number | No | Number of results per page |
| `name` | query | string | No | Filter by partial name match |
| `sort` | query | string | No | Field to sort by |
| `order` | query | string | No | Direction to sort by |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Paginated list of all snapshots | PaginatedSnapshots |

---

## POST `/snapshots` {#daytona/tag/snapshots/POST/snapshots}

**Create a new snapshot**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |

### Request Body

Schema: **CreateSnapshot**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | The name of the snapshot |
| `imageName` | string | No | The image name of the snapshot |
| `entrypoint` | array of string | No | The entrypoint command for the snapshot |
| `general` | boolean | No | Whether the snapshot is general |
| `cpu` | integer | No | CPU cores allocated to the resulting sandbox |
| `gpu` | integer | No | GPU units allocated to the resulting sandbox |
| `memory` | integer | No | Memory allocated to the resulting sandbox in GB |
| `disk` | integer | No | Disk space allocated to the sandbox in GB |
| `buildInfo` | object | No | Build information for the snapshot |
| `regionId` | string | No | ID of the region where the snapshot will be available. Defaults to organization default region if not specified. |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | The snapshot has been successfully created. | SnapshotDto |
| 400 | Bad request - Snapshots with tag ":latest" are not allowed |  |

---

## GET `/snapshots/can-cleanup-image` {#daytona/tag/snapshots/GET/snapshots/can-cleanup-image}

**Check if an image can be cleaned up**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `imageName` | query | string | Yes | Image name with tag to check |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Boolean indicating if image can be cleaned up | boolean |

---

## GET `/snapshots/{id}` {#daytona/tag/snapshots/GET/snapshots/{id}}

**Get snapshot by ID or name**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `id` | path | string | Yes | Snapshot ID or name |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | The snapshot | SnapshotDto |
| 404 | Snapshot not found |  |

---

## DELETE `/snapshots/{id}` {#daytona/tag/snapshots/DELETE/snapshots/{id}}

**Delete snapshot**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `id` | path | string | Yes | Snapshot ID |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Snapshot has been deleted |  |

---

## PATCH `/snapshots/{id}/general` {#daytona/tag/snapshots/PATCH/snapshots/{id}/general}

**Set snapshot general status**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `id` | path | string | Yes | Snapshot ID |

### Request Body

Schema: **SetSnapshotGeneralStatusDto**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `general` | boolean | Yes | Whether the snapshot is general |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Snapshot general status has been set | SnapshotDto |

---

## GET `/snapshots/{id}/build-logs` {#daytona/tag/snapshots/GET/snapshots/{id}/build-logs}

**Get snapshot build logs**

This endpoint is deprecated. Use `getSnapshotBuildLogsUrl` instead.

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `id` | path | string | Yes | Snapshot ID |
| `follow` | query | boolean | No | Whether to follow the logs stream |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 |  |  |

---

## GET `/snapshots/{id}/build-logs-url` {#daytona/tag/snapshots/GET/snapshots/{id}/build-logs-url}

**Get snapshot build logs URL**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `id` | path | string | Yes | Snapshot ID |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | The snapshot build logs URL | Url |

---

## POST `/snapshots/{id}/activate` {#daytona/tag/snapshots/POST/snapshots/{id}/activate}

**Activate a snapshot**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `id` | path | string | Yes | Snapshot ID |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | The snapshot has been successfully activated. | SnapshotDto |
| 400 | Bad request - Snapshot is already active, not in inactive state, or has associated snapshot runners |  |
| 404 | Snapshot not found |  |

---

## POST `/snapshots/{id}/deactivate` {#daytona/tag/snapshots/POST/snapshots/{id}/deactivate}

**Deactivate a snapshot**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `id` | path | string | Yes | Snapshot ID |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 204 | The snapshot has been successfully deactivated. |  |

---
