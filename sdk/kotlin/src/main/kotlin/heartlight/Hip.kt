package heartlight

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import java.time.Instant
import java.util.UUID

const val HIP_VERSION = "0.1"
const val DISCLOSURE = "I am a memorial simulation generated from family-provided records and teaching. I am not the deceased person and I do not claim that their consciousness returned."

@Serializable
data class Provenance(
    @SerialName("artifact_sha256") val artifactSha256: String? = null,
    val producer: String = "heartlight-kotlin",
)

@Serializable
data class HipEvent<T>(
    @SerialName("hip_version") val hipVersion: String = HIP_VERSION,
    @SerialName("event_id") val eventId: String = UUID.randomUUID().toString(),
    @SerialName("project_id") val projectId: String,
    @SerialName("event_type") val eventType: String,
    val timestamp: String = Instant.now().toString(),
    val sequence: Long,
    val source: String,
    val provenance: Provenance = Provenance(),
    val payload: T,
)

@Serializable
data class RhythmSignature(
    val algorithm: String,
    @SerialName("source_sha256") val sourceSha256: String,
    @SerialName("sample_rate") val sampleRate: Int,
    @SerialName("duration_seconds") val durationSeconds: Double,
    @SerialName("beat_times_seconds") val beatTimesSeconds: List<Double>,
    @SerialName("intervals_seconds") val intervalsSeconds: List<Double>,
    @SerialName("estimated_bpm") val estimatedBpm: Double? = null,
    @SerialName("rhythm_digest") val rhythmDigest: String,
)
