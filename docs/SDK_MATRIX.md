# HEARTLIGHT SDK Matrix

HIP v0.1 is the compatibility boundary. A language does not need a first-party SDK to participate; any implementation that can produce/consume the documented JSON envelope and preserve field semantics can interoperate.

## First-party source trees

| Runtime | Path | Intended use | Current scope |
|---|---|---|---|
| Python 3.10+ | `src/heartlight/` | reference engine, CLI, API, cloud adapters | full reference implementation |
| Rust | `sdk/rust/` | native services, embedded/native tooling | HIP event + rhythm types |
| C++20 | `sdk/cpp/` | desktop, embedded, game/audio engines | dependency-light HIP/rhythm types |
| TypeScript | `sdk/typescript/` | browser, Node, Electron | HIP event + rhythm types |
| Swift | `sdk/swift/` | iPhone, iPad, macOS | Codable HIP/rhythm types |
| Kotlin/JVM | `sdk/kotlin/` | Android/JVM | serializable HIP/rhythm types |
| Go | `sdk/go/` | high-throughput backend services | HIP/rhythm types |
| .NET 8 / C# | `sdk/dotnet/` | Windows, Azure-oriented services/apps | JSON HIP/rhythm types |
| Java 17 | `sdk/java/` | JVM enterprise services | HIP/rhythm types |

## What "compatible" means

All SDKs use the same conceptual fields for:

- HIP protocol version
- event ID
- project ID
- event type
- UTC timestamp
- sequence
- source
- provenance
- payload
- rhythm signature

The Python implementation currently owns reference heartbeat extraction. Other SDKs can consume its signature immediately; native extraction implementations should be added behind cross-language conformance fixtures before claiming bit-for-bit equivalence.

## Device coverage

- Web/PWA/Electron: TypeScript
- iOS/iPadOS/macOS: Swift
- Android: Kotlin
- Windows: .NET, C++, Python, Rust
- Linux servers: Python, Rust, C++, Go, Java, .NET, Node
- macOS desktop/server: Swift, Python, Rust, C++, Go, Java, .NET, Node
- embedded/native engines: Rust/C++ depending target

## Adding another language

Implement these two structures first:

1. `HipEvent`
2. `RhythmSignature`

Then add a fixture test that parses the canonical JSON examples in `docs/HEARTLIGHT_PROTOCOL.md`, reserializes them without semantic loss, and validates required fields.

This strategy scales farther than attempting to hand-maintain a bespoke full engine in literally every programming language in existence.
