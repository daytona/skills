

# errors


## Contents

- Index
- func ConvertAPIError
- func ConvertToolboxError
- type DaytonaError
- type DaytonaNotFoundError
- type DaytonaRateLimitError
- type DaytonaTimeoutError
- See Also

```go
import "github.com/daytonaio/daytona/libs/sdk-go/pkg/errors"
```

## Index

- [func ConvertAPIError\(err error, httpResp \*http.Response\) error](https://www.daytona.io/docs/en<#ConvertAPIError>)
- [func ConvertToolboxError\(err error, httpResp \*http.Response\) error](https://www.daytona.io/docs/en<#ConvertToolboxError>)
- [type DaytonaError](https://www.daytona.io/docs/en<#DaytonaError>)
  - [func NewDaytonaError\(message string, statusCode int, headers http.Header\) \*DaytonaError](https://www.daytona.io/docs/en<#NewDaytonaError>)
  - [func \(e \*DaytonaError\) Error\(\) string](https://www.daytona.io/docs/en<#DaytonaError.Error>)
- [type DaytonaNotFoundError](https://www.daytona.io/docs/en<#DaytonaNotFoundError>)
  - [func NewDaytonaNotFoundError\(message string, headers http.Header\) \*DaytonaNotFoundError](https://www.daytona.io/docs/en<#NewDaytonaNotFoundError>)
  - [func \(e \*DaytonaNotFoundError\) Error\(\) string](https://www.daytona.io/docs/en<#DaytonaNotFoundError.Error>)
- [type DaytonaRateLimitError](https://www.daytona.io/docs/en<#DaytonaRateLimitError>)
  - [func NewDaytonaRateLimitError\(message string, headers http.Header\) \*DaytonaRateLimitError](https://www.daytona.io/docs/en<#NewDaytonaRateLimitError>)
  - [func \(e \*DaytonaRateLimitError\) Error\(\) string](https://www.daytona.io/docs/en<#DaytonaRateLimitError.Error>)
- [type DaytonaTimeoutError](https://www.daytona.io/docs/en<#DaytonaTimeoutError>)
  - [func NewDaytonaTimeoutError\(message string\) \*DaytonaTimeoutError](https://www.daytona.io/docs/en<#NewDaytonaTimeoutError>)
  - [func \(e \*DaytonaTimeoutError\) Error\(\) string](https://www.daytona.io/docs/en<#DaytonaTimeoutError.Error>)


<a name="ConvertAPIError"></a>
## func ConvertAPIError

```go
func ConvertAPIError(err error, httpResp *http.Response) error
```

ConvertAPIError converts api\-client\-go errors to SDK error types

<a name="ConvertToolboxError"></a>
## func ConvertToolboxError

```go
func ConvertToolboxError(err error, httpResp *http.Response) error
```

ConvertToolboxError converts toolbox\-api\-client\-go errors to SDK error types

<a name="DaytonaError"></a>
## type DaytonaError

DaytonaError is the base error type for all Daytona SDK errors

```go
type DaytonaError struct {
    Message    string
    StatusCode int
    Headers    http.Header
}
```

<a name="NewDaytonaError"></a>
### func NewDaytonaError

```go
func NewDaytonaError(message string, statusCode int, headers http.Header) *DaytonaError
```

NewDaytonaError creates a new DaytonaError

<a name="DaytonaError.Error"></a>
### func \(\*DaytonaError\) Error

```go
func (e *DaytonaError) Error() string
```


<a name="DaytonaNotFoundError"></a>
## type DaytonaNotFoundError

DaytonaNotFoundError represents a resource not found error \(404\)

```go
type DaytonaNotFoundError struct {
    *DaytonaError
}
```

<a name="NewDaytonaNotFoundError"></a>
### func NewDaytonaNotFoundError

```go
func NewDaytonaNotFoundError(message string, headers http.Header) *DaytonaNotFoundError
```

NewDaytonaNotFoundError creates a new DaytonaNotFoundError

<a name="DaytonaNotFoundError.Error"></a>
### func \(\*DaytonaNotFoundError\) Error

```go
func (e *DaytonaNotFoundError) Error() string
```


<a name="DaytonaRateLimitError"></a>
## type DaytonaRateLimitError

DaytonaRateLimitError represents a rate limit error \(429\)

```go
type DaytonaRateLimitError struct {
    *DaytonaError
}
```

<a name="NewDaytonaRateLimitError"></a>
### func NewDaytonaRateLimitError

```go
func NewDaytonaRateLimitError(message string, headers http.Header) *DaytonaRateLimitError
```

NewDaytonaRateLimitError creates a new DaytonaRateLimitError

<a name="DaytonaRateLimitError.Error"></a>
### func \(\*DaytonaRateLimitError\) Error

```go
func (e *DaytonaRateLimitError) Error() string
```


<a name="DaytonaTimeoutError"></a>
## type DaytonaTimeoutError

DaytonaTimeoutError represents a timeout error

```go
type DaytonaTimeoutError struct {
    *DaytonaError
}
```

<a name="NewDaytonaTimeoutError"></a>
### func NewDaytonaTimeoutError

```go
func NewDaytonaTimeoutError(message string) *DaytonaTimeoutError
```

NewDaytonaTimeoutError creates a new DaytonaTimeoutError

<a name="DaytonaTimeoutError.Error"></a>
### func \(\*DaytonaTimeoutError\) Error

```go
func (e *DaytonaTimeoutError) Error() string
```

## See Also
- [TypeScript SDK - errors](../typescript-sdk/errors.md)
