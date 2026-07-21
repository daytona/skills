

Every Daytona sandbox runs in a **region**: a geographic or logical grouping of compute infrastructure. When creating a sandbox, you can target a specific region, and Daytona schedules the workload on available capacity within that region.

Regions place sandboxes close to your users to reduce latency, keep data within a required jurisdiction, and let you attach your own compute infrastructure.

Regions come in three types, differing in who manages the infrastructure and who can use it:

| **Region type**                            | **Managed by**    | **Infrastructure**                                                          |
| ------------------------------------------ | ----------------- | --------------------------------------------------------------------------- |
| <u>[**Shared**](#shared-regions)</u>       | Daytona           | Shared across all organizations                                             |
| <u>[**Dedicated**](#dedicated-regions)</u> | Daytona           | Provisioned exclusively for a single organization                           |
| <u>[**Custom**](#custom-regions)</u>       | Your organization | <u>[**Bring your own compute (BYOC)**](https://www.daytona.io/docs/en/bring-your-own-compute)</u> |

## Select a region

The sandbox region is set with the `target` parameter. In the SDKs, set it when initializing the client and every sandbox created by that client is scheduled in the specified region. In the API, pass it in the sandbox create request:

```typescript
import { Daytona } from '@daytona/sdk';

// Configure Daytona to use the EU region
const daytona: Daytona = new Daytona({
    target: "eu"
});
```

## Shared regions

Shared regions are managed by Daytona and available to all organizations.

| **Region**    | **Target** |
| ------------- | ---------- |
| United States | **`us`**   |
| Europe        | **`eu`**   |

## Dedicated regions

Dedicated regions are managed by Daytona and provisioned exclusively for a single organization. The infrastructure is not shared with other organizations, and Daytona operates it as a managed service.
> **Note:**
> Contact [sales@daytona.io](mailto:sales@daytona.io) to set up a dedicated region for your organization.

## Custom regions

Custom regions run on compute that your organization provides and manages. Attach your own machines through [bring your own compute (BYOC)](https://www.daytona.io/docs/en/bring-your-own-compute) to control data locality, compliance, and infrastructure configuration, and scale capacity independently within each region.

Custom regions have no limits on concurrent resource usage: capacity is bounded only by the compute you attach.

## See Also
- [Python SDK - regions](../python-sdk/regions.md)
