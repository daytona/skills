# Webhooks API

## POST `/webhooks/organizations/{organizationId}/app-portal-access` {#daytona/tag/webhooks/POST/webhooks/organizations/{organizationId}/app-portal-access}

**Get Svix Consumer App Portal access for an organization**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `organizationId` | path | string | Yes |  |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | App Portal access generated successfully | WebhookAppPortalAccess |

---

## POST `/webhooks/organizations/{organizationId}/send` {#daytona/tag/webhooks/POST/webhooks/organizations/{organizationId}/send}

**Send a webhook message to an organization**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `organizationId` | path | string | Yes |  |

### Request Body

Schema: **SendWebhookDto**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `eventType` | object | Yes | The type of event being sent |
| `payload` | object | Yes | The payload data to send |
| `eventId` | string | No | Optional event ID for idempotency |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Webhook message sent successfully |  |

---

## GET `/webhooks/organizations/{organizationId}/messages/{messageId}/attempts` {#daytona/tag/webhooks/GET/webhooks/organizations/{organizationId}/messages/{messageId}/attempts}

**Get delivery attempts for a webhook message**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `organizationId` | path | string | Yes |  |
| `messageId` | path | string | Yes |  |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | List of delivery attempts | array |

---

## GET `/webhooks/status` {#daytona/tag/webhooks/GET/webhooks/status}

**Get webhook service status**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Webhook service status | WebhookController_getStatus_200_response |

---

## GET `/webhooks/organizations/{organizationId}/initialization-status` {#daytona/tag/webhooks/GET/webhooks/organizations/{organizationId}/initialization-status}

**Get webhook initialization status for an organization**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `organizationId` | path | string | Yes |  |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Webhook initialization status | WebhookInitializationStatus |
| 404 | Webhook initialization status not found |  |

---

## POST `/webhooks/organizations/{organizationId}/initialize` {#daytona/tag/webhooks/POST/webhooks/organizations/{organizationId}/initialize}

**Initialize webhooks for an organization**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `X-Daytona-Organization-ID` | header | string | No | Use with JWT to specify the organization ID |
| `organizationId` | path | string | Yes |  |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 201 | Webhooks initialized successfully |  |
| 403 | User does not have access to this organization |  |
| 404 | Organization not found |  |

---
