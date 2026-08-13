use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use sha2::{Digest, Sha256};
use uuid::Uuid;

pub const HIP_VERSION: &str = "0.1";
pub const DISCLOSURE: &str = "I am a memorial simulation generated from family-provided records and teaching. I am not the deceased person and I do not claim that their consciousness returned.";

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Provenance {
    pub artifact_sha256: Option<String>,
    pub producer: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HipEvent {
    pub hip_version: String,
    pub event_id: Uuid,
    pub project_id: Uuid,
    pub event_type: String,
    pub timestamp: DateTime<Utc>,
    pub sequence: u64,
    pub source: String,
    pub provenance: Provenance,
    pub payload: Value,
}

impl HipEvent {
    pub fn new(project_id: Uuid, event_type: impl Into<String>, sequence: u64, source: impl Into<String>, payload: Value) -> Self {
        Self {
            hip_version: HIP_VERSION.to_string(),
            event_id: Uuid::new_v4(),
            project_id,
            event_type: event_type.into(),
            timestamp: Utc::now(),
            sequence,
            source: source.into(),
            provenance: Provenance { artifact_sha256: None, producer: "heartlight-rust".to_string() },
            payload,
        }
    }

    pub fn canonical_digest(&self) -> Result<String, serde_json::Error> {
        let encoded = serde_json::to_vec(self)?;
        Ok(format!("{:x}", Sha256::digest(encoded)))
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RhythmSignature {
    pub algorithm: String,
    pub source_sha256: String,
    pub sample_rate: u32,
    pub duration_seconds: f64,
    pub beat_times_seconds: Vec<f64>,
    pub intervals_seconds: Vec<f64>,
    pub estimated_bpm: Option<f64>,
    pub rhythm_digest: String,
}
