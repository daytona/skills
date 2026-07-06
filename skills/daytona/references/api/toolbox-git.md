# Git API


## Contents

- POST `/git/add`
- GET `/git/branches`
- POST `/git/branches`
- DELETE `/git/branches`
- POST `/git/checkout`
- POST `/git/clone`
- POST `/git/commit`
- GET `/git/config`
- POST `/git/config`
- POST `/git/config/user`
- POST `/git/credentials`
- GET `/git/history`
- POST `/git/init`
- POST `/git/pull`
- POST `/git/push`
- GET `/git/remotes`
- POST `/git/remotes`
- POST `/git/reset`
- POST `/git/restore`
- GET `/git/status`

## POST `/git/add` {#daytona-toolbox/tag/git/POST/git/add}

**Add files to Git staging**

Add files to the Git staging area

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Add files request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## GET `/git/branches` {#daytona-toolbox/tag/git/GET/git/branches}

**List branches**

Get a list of all branches in the Git repository

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `path` | query | string | Yes | Repository path |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/git/branches` {#daytona-toolbox/tag/git/POST/git/branches}

**Create a new branch**

Create a new branch in the Git repository

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Create branch request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 201 | Created |  |

---

## DELETE `/git/branches` {#daytona-toolbox/tag/git/DELETE/git/branches}

**Delete a branch**

Delete a branch from the Git repository

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Delete branch request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 204 | No Content |  |

---

## POST `/git/checkout` {#daytona-toolbox/tag/git/POST/git/checkout}

**Checkout branch or commit**

Switch to a different branch or commit in the Git repository

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Checkout request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/git/clone` {#daytona-toolbox/tag/git/POST/git/clone}

**Clone a Git repository**

Clone a Git repository to the specified path. Defaults to strict TLS verification; set insecure_skip_tls=true to skip verification for self-signed or private-CA Git servers.

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Clone repository request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/git/commit` {#daytona-toolbox/tag/git/POST/git/commit}

**Commit changes**

Commit staged changes to the Git repository

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Commit request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## GET `/git/config` {#daytona-toolbox/tag/git/GET/git/config}

**Get a Git config value**

Get a Git config value at the given scope (null when unset)

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `key` | query | string | Yes | Config key (e.g. user.name) |
| `path` | query | string | No | Repository path (required for local scope) |
| `scope` | query | string | No | Config scope: global (default), local or system |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/git/config` {#daytona-toolbox/tag/git/POST/git/config}

**Set a Git config value**

Set a Git config key/value at the given scope

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Set config request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/git/config/user` {#daytona-toolbox/tag/git/POST/git/config/user}

**Configure Git user**

Configure the Git user name and email at the given scope

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Configure user request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/git/credentials` {#daytona-toolbox/tag/git/POST/git/credentials}

**Authenticate Git**

Persist Git credentials globally via the credential store. Stores the password in plaintext on disk.

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Authenticate request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## GET `/git/history` {#daytona-toolbox/tag/git/GET/git/history}

**Get commit history**

Get the commit history of the Git repository

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `path` | query | string | Yes | Repository path |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/git/init` {#daytona-toolbox/tag/git/POST/git/init}

**Initialize a Git repository**

Initialize a new Git repository at the specified path

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Init repository request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 201 | Created |  |

---

## POST `/git/pull` {#daytona-toolbox/tag/git/POST/git/pull}

**Pull changes from remote**

Pull changes from the remote Git repository

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Pull request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/git/push` {#daytona-toolbox/tag/git/POST/git/push}

**Push changes to remote**

Push local changes to the remote Git repository

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Push request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## GET `/git/remotes` {#daytona-toolbox/tag/git/GET/git/remotes}

**List remotes**

List the remotes configured in the Git repository

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `path` | query | string | Yes | Repository path |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/git/remotes` {#daytona-toolbox/tag/git/POST/git/remotes}

**Add a remote**

Add (or overwrite) a remote in the Git repository

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Add remote request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 201 | Created |  |

---

## POST `/git/reset` {#daytona-toolbox/tag/git/POST/git/reset}

**Reset repository**

Reset the current HEAD to the specified state

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Reset request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## POST `/git/restore` {#daytona-toolbox/tag/git/POST/git/restore}

**Restore files**

Restore working tree files or unstage changes

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `request` | body | string | Yes | Restore request |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---

## GET `/git/status` {#daytona-toolbox/tag/git/GET/git/status}

**Get Git status**

Get the Git status of the repository at the specified path

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `path` | query | string | Yes | Repository path |

### Responses

| Status | Description | Schema |
|--------|-------------|--------|
| 200 | OK |  |

---
