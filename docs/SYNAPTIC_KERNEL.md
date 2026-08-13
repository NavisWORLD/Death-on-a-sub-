# HEARTLIGHT Synaptic Kernel v1.0

The Synaptic Kernel is the language-neutral learning primitive shared by the HEARTLIGHT SDKs. It is deliberately small, deterministic, dependency-light, and independent of any claim about biology or consciousness.

## Update rule

For state `(w, e)`, input `(pre, post, reward)`, and configuration `(learning_rate, decay, trace_decay, min_weight, max_weight)`:

```text
e_next = trace_decay * e + pre * post
w_raw  = (1 - decay) * w + learning_rate * reward * e_next
w_next = clamp(w_raw, min_weight, max_weight)
```

Defaults:

```text
learning_rate = 0.08
decay          = 0.002
trace_decay    = 0.9
min_weight     = -1.0
max_weight     = 1.0
```

All first-party implementations use IEEE-754 binary64 (`double`/`f64`/`Double`/Python `float`) and are checked against `sdk/conformance/synaptic-v1.json` with an absolute tolerance of `1e-12`.

## First-party implementations

- Python: `src/heartlight/synaptic.py`
- Rust: `sdk/rust/src/synaptic.rs`
- C++20: `sdk/cpp/include/heartlight/synaptic.hpp`
- C11 ABI: `sdk/c/`
- Go: `sdk/go/synaptic.go`
- TypeScript/JavaScript: `sdk/typescript/src/synaptic.ts`
- Java 17: `sdk/java/.../SynapticKernel.java`
- Kotlin/JVM: `sdk/kotlin/.../SynapticKernel.kt`
- Swift: `sdk/swift/Sources/HeartlightHIP/SynapticKernel.swift`
- .NET 8 / C#: `sdk/dotnet/Heartlight.Hip/SynapticKernel.cs`

## Why C matters

The C implementation is the universal native boundary. Languages with C FFI can bind the kernel without copying the algorithm. Examples include Zig, Julia, LuaJIT, Ruby native extensions, PHP FFI, JNI/JNA, Dart FFI, Python ctypes/cffi, Node native addons, Godot/GDExtension, Unity native plugins, Unreal modules, and embedded firmware.

## Compatibility rule

A port is HEARTLIGHT Synaptic Kernel v1.0 compatible only if it:

1. performs operations in the documented order;
2. rejects non-finite values and invalid bounds/rates;
3. clamps after decay and reward-modulated learning;
4. matches the canonical fixture within `1e-12` for binary64 implementations;
5. declares any lower-precision deviation for constrained hardware.

The kernel is a computational learning primitive. It does not establish a biological neural mechanism, recover a person, or prove consciousness transfer.
