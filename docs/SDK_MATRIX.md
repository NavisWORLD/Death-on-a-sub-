# HEARTLIGHT SDK Matrix

HIP v0.1 is the data compatibility boundary. Synaptic Kernel v1.0 is the deterministic learning compatibility boundary. A language can participate through native first-party code, the documented JSON structures, or the C ABI.

## First-party source trees

| Runtime | Path | HIP | Synaptic v1 | Intended use |
|---|---|---:|---:|---|
| Python 3.10+ | `src/heartlight/` | ✅ | ✅ | reference engine, CLI, API, desktop |
| Rust | `sdk/rust/` | ✅ | ✅ | native services, embedded/native tooling |
| C++20 | `sdk/cpp/` | ✅ | ✅ | desktop, embedded, game/audio engines |
| C11 | `sdk/c/` | ABI | ✅ | universal FFI/native boundary |
| TypeScript/JavaScript | `sdk/typescript/` | ✅ | ✅ | browser, Node, Electron |
| Swift | `sdk/swift/` | ✅ | ✅ | iPhone, iPad, macOS |
| Kotlin/JVM | `sdk/kotlin/` | ✅ | ✅ | Android/JVM |
| Go | `sdk/go/` | ✅ | ✅ | backend services |
| .NET 8 / C# | `sdk/dotnet/` | ✅ | ✅ | Windows, Azure, Unity-oriented apps/services |
| Java 17 | `sdk/java/` | ✅ | ✅ | JVM enterprise services |

## Cross-language conformance

`sdk/conformance/synaptic-v1.json` is the canonical numerical fixture. Binary64 implementations must match it within `1e-12`. `.github/workflows/sdk-conformance.yml` compiles and tests the native implementations on GitHub Actions.

## Other languages

Do not fork the math unless necessary. Bind the C11 ABI in `sdk/c/` from Zig, Julia, LuaJIT, Ruby, PHP FFI, Dart, JNI/JNA, Python ctypes/cffi, Node native addons, Godot, Unity, Unreal, or another C-FFI-capable runtime. A direct native port should preserve operation order and add the same conformance fixture.

## Device coverage

- Web/PWA/Electron: TypeScript
- iOS/iPadOS/macOS: Swift
- Android: Kotlin
- Windows: .NET, C++, Python, Rust, C
- Linux servers: Python, Rust, C/C++, Go, Java, .NET, Node
- macOS desktop/server: Swift, Python, Rust, C/C++, Go, Java, .NET, Node
- embedded/native engines: Rust/C/C++ depending target

See `docs/SYNAPTIC_KERNEL.md` for the update rule and compatibility contract.
