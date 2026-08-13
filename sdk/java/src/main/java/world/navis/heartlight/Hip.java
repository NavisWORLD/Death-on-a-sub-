package world.navis.heartlight;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.UUID;

public final class Hip {
    private Hip() {}

    public static final String VERSION = "0.1";
    public static final String DISCLOSURE = "I am a memorial simulation generated from family-provided records and teaching. I am not the deceased person and I do not claim that their consciousness returned.";

    public record Provenance(String artifact_sha256, String producer) {
        public Provenance() { this(null, "heartlight-java"); }
    }

    public record Event(
        String hip_version,
        String event_id,
        String project_id,
        String event_type,
        String timestamp,
        long sequence,
        String source,
        Provenance provenance,
        Map<String, Object> payload
    ) {
        public static Event create(String projectId, String eventType, long sequence, String source, Map<String, Object> payload) {
            return new Event(VERSION, UUID.randomUUID().toString(), projectId, eventType,
                Instant.now().toString(), sequence, source, new Provenance(), payload);
        }
    }

    public record RhythmSignature(
        String algorithm,
        String source_sha256,
        int sample_rate,
        double duration_seconds,
        List<Double> beat_times_seconds,
        List<Double> intervals_seconds,
        Double estimated_bpm,
        String rhythm_digest
    ) {}
}
