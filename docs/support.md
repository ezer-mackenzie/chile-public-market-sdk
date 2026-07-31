# Support and deprecation policy

## Supported Python versions

The SDK supports Python 3.12, 3.13, and 3.14. A Python version may be removed
only in a new SDK major release unless that Python version has reached end of
life and can no longer receive security fixes.

## Release support

The latest minor release in the current major series receives compatible bug
and security fixes. Older minor releases may receive critical security fixes
when a safe backport is practical. Pre-release versions before `1.0.0` are not
supported after the stable release.

## Compatibility promise

Starting with `1.0.0`, documented top-level imports, client and SDK classes,
public methods, parameters, models, enums, exceptions, and serialized English
field names are stable within the `1.x` series. Removing or renaming them
requires a new major version.

Additive endpoints, optional model fields, enum members, and optional keyword
parameters may be introduced in minor releases. Mercado Público may add
unknown response fields at any time; models preserve them through Pydantic's
`extra="allow"` policy.

Modules and names beginning with an underscore, and modules under
`core/constants/`, are internal implementation details unless another page
explicitly documents them as public.

## Deprecations

A public API scheduled for removal is documented in the changelog and emits a
`DeprecationWarning` for at least one minor release before removal in the next
major release. Security or correctness issues that make an API unsafe may
require faster removal and will be called out prominently in a security
advisory and migration guide.

## Upstream compatibility

ChileCompra's upstream v1 and v2 contracts are independent from the SDK's
Semantic Versioning. Compatible upstream additions do not require a major SDK
release. An upstream breaking change that forces a documented Python API break
is handled in a new SDK major version.
