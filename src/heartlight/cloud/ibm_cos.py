from __future__ import annotations

import os
from pathlib import Path


def sync_directory(root: str | Path) -> int:
    """Mirror a HEARTLIGHT vault to IBM Cloud Object Storage.

    Required environment variables:
      HEARTLIGHT_IBM_COS_API_KEY
      HEARTLIGHT_IBM_COS_INSTANCE_CRN
      HEARTLIGHT_IBM_COS_ENDPOINT
      HEARTLIGHT_IBM_COS_BUCKET
    """
    try:
        import ibm_boto3
        from ibm_botocore.client import Config
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("Install IBM support with: pip install -e '.[ibm]'") from exc

    api_key = os.environ.get("HEARTLIGHT_IBM_COS_API_KEY")
    instance_crn = os.environ.get("HEARTLIGHT_IBM_COS_INSTANCE_CRN")
    endpoint = os.environ.get("HEARTLIGHT_IBM_COS_ENDPOINT")
    bucket = os.environ.get("HEARTLIGHT_IBM_COS_BUCKET")
    if not all((api_key, instance_crn, endpoint, bucket)):
        raise RuntimeError(
            "Set HEARTLIGHT_IBM_COS_API_KEY, HEARTLIGHT_IBM_COS_INSTANCE_CRN, "
            "HEARTLIGHT_IBM_COS_ENDPOINT, and HEARTLIGHT_IBM_COS_BUCKET"
        )

    cos = ibm_boto3.resource(
        "s3",
        ibm_api_key_id=api_key,
        ibm_service_instance_id=instance_crn,
        config=Config(signature_version="oauth"),
        endpoint_url=endpoint,
    )

    source_root = Path(root).expanduser().resolve()
    uploaded = 0
    for path in sorted(p for p in source_root.rglob("*") if p.is_file()):
        key = path.relative_to(source_root).as_posix()
        cos.Bucket(bucket).upload_file(str(path), key)
        uploaded += 1
    return uploaded
