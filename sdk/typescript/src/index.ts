export const HIP_VERSION = "0.1" as const;
export const DISCLOSURE = "I am a memorial simulation generated from family-provided records and teaching. I am not the deceased person and I do not claim that their consciousness returned.";

export type Provenance = {
  artifact_sha256?: string;
  producer: string;
};

export type HipEvent<T = Record<string, unknown>> = {
  hip_version: typeof HIP_VERSION;
  event_id: string;
  project_id: string;
  event_type: string;
  timestamp: string;
  sequence: number;
  source: string;
  provenance: Provenance;
  payload: T;
};

export type RhythmSignature = {
  algorithm: string;
  source_sha256: string;
  sample_rate: number;
  duration_seconds: number;
  beat_times_seconds: number[];
  intervals_seconds: number[];
  estimated_bpm: number | null;
  rhythm_digest: string;
};

export function createEvent<T>(args: {
  projectId: string;
  eventType: string;
  sequence: number;
  source: string;
  payload: T;
  artifactSha256?: string;
}): HipEvent<T> {
  return {
    hip_version: HIP_VERSION,
    event_id: crypto.randomUUID(),
    project_id: args.projectId,
    event_type: args.eventType,
    timestamp: new Date().toISOString(),
    sequence: args.sequence,
    source: args.source,
    provenance: {
      artifact_sha256: args.artifactSha256,
      producer: "heartlight-typescript",
    },
    payload: args.payload,
  };
}
