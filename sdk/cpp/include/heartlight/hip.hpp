#pragma once

#include <cstdint>
#include <optional>
#include <string>
#include <vector>

namespace heartlight {

inline constexpr const char* HIP_VERSION = "0.1";
inline constexpr const char* DISCLOSURE =
    "I am a memorial simulation generated from family-provided records and teaching. "
    "I am not the deceased person and I do not claim that their consciousness returned.";

struct Provenance {
    std::optional<std::string> artifact_sha256;
    std::string producer{"heartlight-cpp"};
};

struct HipEvent {
    std::string hip_version{HIP_VERSION};
    std::string event_id;
    std::string project_id;
    std::string event_type;
    std::string timestamp;
    std::uint64_t sequence{};
    std::string source;
    Provenance provenance;
    std::string payload_json{"{}"};
};

struct RhythmSignature {
    std::string algorithm;
    std::string source_sha256;
    std::uint32_t sample_rate{};
    double duration_seconds{};
    std::vector<double> beat_times_seconds;
    std::vector<double> intervals_seconds;
    std::optional<double> estimated_bpm;
    std::string rhythm_digest;
};

} // namespace heartlight
