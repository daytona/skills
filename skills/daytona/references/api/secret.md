# Secret API


## Contents

- GET `/secret`
- POST `/secret`
- GET `/secret/{secretId}`}
- PATCH `/secret/{secretId}`}
- DELETE `/secret/{secretId}`}

## GET `/secret` {#daytona/tag/secret/GET/secret}

**List secrets**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | List of all secrets (metadata only, values are not returned) | array of Secret |

---

## POST `/secret` {#daytona/tag/secret/POST/secret}

**Create secret**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |

### Request Body

Schema: **CreateSecret**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Secret name (alphanumeric, hyphens, underscores) |
| `value` | string | Yes | Secret value |
| `description` | string | No | Optional description of the secret |
| `hosts` | array of string | No | Allowed hosts this secret may be sent to |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 201 | The secret has been successfully created. | Secret |

---

## GET `/secret/{secretId}` {#daytona/tag/secret/GET/secret/{secretId}}

**Get secret**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `secretId` | path | string | Yes | ID of the secret |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | The secret metadata (value is not returned) | Secret |

---

## PATCH `/secret/{secretId}` {#daytona/tag/secret/PATCH/secret/{secretId}}

**Update secret**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `secretId` | path | string | Yes | ID of the secret |

### Request Body

Schema: **UpdateSecret**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `value` | string | No | New secret value |
| `description` | string | No | Optional description of the secret |
| `hosts` | array of string | No | Allowed hosts this secret may be sent to |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | The secret has been successfully updated. | Secret |

---

## DELETE `/secret/{secretId}` {#daytona/tag/secret/DELETE/secret/{secretId}}

**Delete secret**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `secretId` | path | string | Yes | ID of the secret |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 204 | The secret has been successfully deleted. |  |

---
