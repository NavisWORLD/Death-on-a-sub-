# HEARTLIGHT Cross-Language SDKs

HEARTLIGHT has two interoperability layers:

1. **HIP** — shared event/provenance/rhythm structures.
2. **Synaptic Kernel v1.0** — shared deterministic learning behavior.

## Native SDKs

| Language | HIP | Synaptic Kernel | Native package/build |
|---|---:|---:|---|
| Python | ✅ | ✅ | `pip` / `pyproject.toml` |
| Rust | ✅ | ✅ | Cargo |
| C++20 | ✅ | ✅ | CMake/header-only kernel |
| C11 | via structs/FFI | ✅ | CMake/static library |
| TypeScript + JavaScript | ✅ | ✅ | npm/tsc |
| Go | ✅ | ✅ | Go modules |
| Java 17 | ✅ | ✅ | Maven |
| Kotlin/JVM | ✅ | ✅ | Gradle |
| Swift | ✅ | ✅ | Swift Package Manager |
| C# / .NET 8 | ✅ | ✅ | dotnet |

The C ABI provides the bridge for additional languages that support C FFI. See `docs/SYNAPTIC_KERNEL.md` and `sdk/conformance/synaptic-v1.json`.
