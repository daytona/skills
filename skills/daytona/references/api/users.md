# Users API

## GET `/users/me` {#daytona/tag/users/GET/users/me}

**Get authenticated user**

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | User details | User |

---

## GET `/users` {#daytona/tag/users/GET/users}

**List all users**

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 |  |  |

---

## POST `/users` {#daytona/tag/users/POST/users}

**Create user**

### Request Body

Schema: **CreateUser**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes |  |
| `name` | string | Yes |  |
| `email` | string | No |  |
| `personalOrganizationQuota` | [CreateOrganizationQuota](#schema-createorganizationquota) | No |  |
| `personalOrganizationDefaultRegionId` | string | No |  |
| `role` | string | No |  |
| `emailVerified` | boolean | No |  |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 201 |  |  |

---

## POST `/users/{id}/regenerate-key-pair` {#daytona/tag/users/POST/users/{id}/regenerate-key-pair}

**Regenerate user key pair**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `id` | path | string | Yes |  |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 201 |  |  |

---

## GET `/users/account-providers` {#daytona/tag/users/GET/users/account-providers}

**Get available account providers**

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Available account providers | array of AccountProvider |

---

## POST `/users/linked-accounts` {#daytona/tag/users/POST/users/linked-accounts}

**Link account**

### Request Body

Schema: **CreateLinkedAccount**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `provider` | string | Yes | The authentication provider of the secondary account |
| `userId` | string | Yes | The user ID of the secondary account |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 204 | Account linked successfully |  |

---

## DELETE `/users/linked-accounts/{provider}/{providerUserId}` {#daytona/tag/users/DELETE/users/linked-accounts/{provider}/{providerUserId}}

**Unlink account**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `provider` | path | string | Yes |  |
| `providerUserId` | path | string | Yes |  |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 204 | Account unlinked successfully |  |

---

## POST `/users/mfa/sms/enroll` {#daytona/tag/users/POST/users/mfa/sms/enroll}

**Enroll in SMS MFA**

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | SMS MFA enrollment URL | string |

---

## GET `/users/{id}` {#daytona/tag/users/GET/users/{id}}

**Get user by ID**

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `id` | path | string | Yes |  |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | User details | User |

---
