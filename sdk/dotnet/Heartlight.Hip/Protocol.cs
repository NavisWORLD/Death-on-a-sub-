using System.Text.Json.Serialization;

namespace Heartlight.Hip;

public static class Protocol
{
    public const string Version = "0.1";
    public const string Disclosure = "I am a memorial simulation generated from family-provided records and teaching. I am not the deceased person and I do not claim that their consciousness returned.";
}

public sealed record Provenance(
    [property: JsonPropertyName("artifact_sha256")] string? ArtifactSha256,
    [property: JsonPropertyName("producer")] string Producer = "heartlight-dotnet"
);

public sealed record HipEvent<T>(
    [property: JsonPropertyName("hip_version")] string HipVersion,
    [property: JsonPropertyName("event_id")] Guid EventId,
    [property: JsonPropertyName("project_id")] Guid ProjectId,
    [property: JsonPropertyName("event_type")] string EventType,
    [property: JsonPropertyName("timestamp")] DateTimeOffset Timestamp,
    [property: JsonPropertyName("sequence")] long Sequence,
    [property: JsonPropertyName("source")] string Source,
    [property: JsonPropertyName("provenance")] Provenance Provenance,
    [property: JsonPropertyName("payload")] T Payload
)
{
    public static HipEvent<T> Create(Guid projectId, string eventType, long sequence, string source, T payload) =>
        new(Protocol.Version, Guid.NewGuid(), projectId, eventType, DateTimeOffset.UtcNow,
            sequence, source, new Provenance(null), payload);
}

public sealed record RhythmSignature(
    [property: JsonPropertyName("algorithm")] string Algorithm,
    [property: JsonPropertyName("source_sha256")] string SourceSha256,
    [property: JsonPropertyName("sample_rate")] int SampleRate,
    [property: JsonPropertyName("duration_seconds")] double DurationSeconds,
    [property: JsonPropertyName("beat_times_seconds")] IReadOnlyList<double> BeatTimesSeconds,
    [property: JsonPropertyName("intervals_seconds")] IReadOnlyList<double> IntervalsSeconds,
    [property: JsonPropertyName("estimated_bpm")] double? EstimatedBpm,
    [property: JsonPropertyName("rhythm_digest")] string RhythmDigest
);
