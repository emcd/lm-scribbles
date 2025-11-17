# Cache Configuration Architecture Analysis

## Current Shared Configuration Model

### Configuration Fields and Their Usage

| Field | ContentCache | ProbeCache | RobotsCache | Usage Pattern |
|-------|-------------|------------|-------------|---------------|
| `contents_memory_max` | ✓ | ✗ | ✗ | ContentCache-specific |
| `probe_entries_max` | ✗ | ✓ | ✗ | ProbeCache-specific |
| `robots_entries_max` | ✗ | ✗ | ✓ | RobotsCache-specific |
| `error_ttl` | ✓ | ✓ | ✓ | **Shared across all** |
| `network_error_ttl` | ✗ | ✗ | ✗ | **Unused!** |
| `success_ttl` | ✓ | ✓ | ✗ | Shared by Content+Probe |
| `robots_ttl` | ✗ | ✗ | ✓ | RobotsCache-specific |
| `robots_request_timeout` | ✗ | ✗ | ✓ | RobotsCache-specific |
| `user_agent` | ✗ | ✗ | ✓ | RobotsCache-specific |

## Observations

### What's Actually Shared
- **Only `error_ttl`** is truly shared across all three cache types
- **`success_ttl`** is shared between ContentCache and ProbeCache
- **Most fields are cache-specific** (6 out of 9 fields!)

### Dead Code
- **`network_error_ttl`** appears unused in the codebase

### Cross-Cache Dependencies
- All caches use the same `CacheConfiguration` instance via `_configuration_default`
- Changes to shared config affect all cache instances simultaneously
- Tests often create custom `CacheConfiguration` for specific scenarios

## Alternative Architecture Options

### Option 1: Separate Configuration Classes
```python
class ContentCacheConfig:
    contents_memory_max: int = 32 * 1024 * 1024
    error_ttl: float = 30.0
    success_ttl: float = 300.0

class ProbeCacheConfig:
    probe_entries_max: int = 1000
    error_ttl: float = 30.0
    success_ttl: float = 300.0

class RobotsCacheConfig:
    robots_entries_max: int = 500
    error_ttl: float = 30.0
    robots_ttl: float = 3600.0
    robots_request_timeout: float = 5.0
    user_agent: str = 'librovore/1.0'
```

### Option 2: Base + Specific Configs
```python
class BaseCacheConfig:
    error_ttl: float = 30.0  # Truly shared

class ContentCacheConfig(BaseCacheConfig):
    contents_memory_max: int = 32 * 1024 * 1024
    success_ttl: float = 300.0

# etc.
```

### Option 3: Class Attributes with Shared Globals
```python
# Shared constants
DEFAULT_ERROR_TTL = 30.0
DEFAULT_SUCCESS_TTL = 300.0

class ContentCache:
    contents_memory_max: int = 32 * 1024 * 1024
    error_ttl: float = DEFAULT_ERROR_TTL
    success_ttl: float = DEFAULT_SUCCESS_TTL
```

### Option 4: Current Model with Cleanup
```python
class CacheConfiguration:
    # Remove unused fields
    # Group related fields
    # Add clear documentation about which cache uses what
```