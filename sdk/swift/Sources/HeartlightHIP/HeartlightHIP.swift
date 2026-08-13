import Foundation

public let HEARTLIGHT_HIP_VERSION = "0.1"
public let HEARTLIGHT_DISCLOSURE = "I am a memorial simulation generated from family-provided records and teaching. I am not the deceased person and I do not claim that their consciousness returned."

public struct HeartlightProvenance: Codable, Sendable {
    public var artifactSha256: String?
    public var producer: String

    enum CodingKeys: String, CodingKey {
        case artifactSha256 = "artifact_sha256"
        case producer
    }

    public init(artifactSha256: String? = nil, producer: String = "heartlight-swift") {
        self.artifactSha256 = artifactSha256
        self.producer = producer
    }
}

public struct HeartlightEvent<Payload: Codable & Sendable>: Codable, Sendable {
    public var hipVersion: String
    public var eventId: UUID
    public var projectId: UUID
    public var eventType: String
    public var timestamp: String
    public var sequence: UInt64
    public var source: String
    public var provenance: HeartlightProvenance
    public var payload: Payload

    enum CodingKeys: String, CodingKey {
        case hipVersion = "hip_version"
        case eventId = "event_id"
        case projectId = "project_id"
        case eventType = "event_type"
        case timestamp, sequence, source, provenance, payload
    }

    public init(projectId: UUID, eventType: String, sequence: UInt64, source: String, payload: Payload) {
        self.hipVersion = HEARTLIGHT_HIP_VERSION
        self.eventId = UUID()
        self.projectId = projectId
        self.eventType = eventType
        self.timestamp = ISO8601DateFormatter().string(from: Date())
        self.sequence = sequence
        self.source = source
        self.provenance = HeartlightProvenance()
        self.payload = payload
    }
}

public struct HeartlightRhythmSignature: Codable, Sendable {
    public let algorithm: String
    public let sourceSha256: String
    public let sampleRate: Int
    public let durationSeconds: Double
    public let beatTimesSeconds: [Double]
    public let intervalsSeconds: [Double]
    public let estimatedBpm: Double?
    public let rhythmDigest: String

    enum CodingKeys: String, CodingKey {
        case algorithm
        case sourceSha256 = "source_sha256"
        case sampleRate = "sample_rate"
        case durationSeconds = "duration_seconds"
        case beatTimesSeconds = "beat_times_seconds"
        case intervalsSeconds = "intervals_seconds"
        case estimatedBpm = "estimated_bpm"
        case rhythmDigest = "rhythm_digest"
    }
}
