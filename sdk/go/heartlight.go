package heartlight

import "time"

const HIPVersion = "0.1"
const Disclosure = "I am a memorial simulation generated from family-provided records and teaching. I am not the deceased person and I do not claim that their consciousness returned."

type Provenance struct {
	ArtifactSHA256 string `json:"artifact_sha256,omitempty"`
	Producer       string `json:"producer"`
}

type HipEvent[T any] struct {
	HIPVersion string     `json:"hip_version"`
	EventID    string     `json:"event_id"`
	ProjectID  string     `json:"project_id"`
	EventType  string     `json:"event_type"`
	Timestamp  time.Time  `json:"timestamp"`
	Sequence   uint64     `json:"sequence"`
	Source     string     `json:"source"`
	Provenance Provenance `json:"provenance"`
	Payload    T          `json:"payload"`
}

type RhythmSignature struct {
	Algorithm            string    `json:"algorithm"`
	SourceSHA256         string    `json:"source_sha256"`
	SampleRate           int       `json:"sample_rate"`
	DurationSeconds      float64   `json:"duration_seconds"`
	BeatTimesSeconds     []float64 `json:"beat_times_seconds"`
	IntervalsSeconds     []float64 `json:"intervals_seconds"`
	EstimatedBPM         *float64  `json:"estimated_bpm"`
	RhythmDigest         string    `json:"rhythm_digest"`
}
