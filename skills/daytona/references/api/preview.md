# Preview API

## GET `/preview/{sandboxId}/public` {#daytona/tag/preview/GET/preview/{sandboxId}/public}

**Check if sandbox is public**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `sandboxId` | path | string | Yes | ID of the sandbox |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Public status of the sandbox | boolean |

---

## GET `/preview/{sandboxId}/preview-warning` {#daytona/tag/preview/GET/preview/{sandboxId}/preview-warning}

**Check if the preview warning page is enabled for the sandbox**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `sandboxId` | path | string | Yes | ID of the sandbox, or a signed preview URL token (requires the port query param) |
| `port` | query | number | No | Port the signed preview URL token was issued for. Required when sandboxId is a signed token. |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Whether the preview warning page is enabled for the sandbox | PreviewWarning |

---

## GET `/preview/{sandboxId}/validate/{authToken}` {#daytona/tag/preview/GET/preview/{sandboxId}/validate/{authToken}}

**Check if sandbox auth token is valid**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `sandboxId` | path | string | Yes | ID of the sandbox |
| `authToken` | path | string | Yes | Auth token of the sandbox |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Sandbox auth token validation status | boolean |

---

## GET `/preview/{sandboxId}/access` {#daytona/tag/preview/GET/preview/{sandboxId}/access}

**Check if user has access to the sandbox**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `sandboxId` | path | string | Yes |  |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | User access status to the sandbox | boolean |

---

## GET `/preview/{signedPreviewToken}/{port}/sandbox-id` {#daytona/tag/preview/GET/preview/{signedPreviewToken}/{port}/sandbox-id}

**Get sandbox ID from signed preview URL token**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `signedPreviewToken` | path | string | Yes | Signed preview URL token |
| `port` | path | number | Yes | Port number to get sandbox ID from signed preview URL token |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Sandbox ID from signed preview URL token | string |

---
