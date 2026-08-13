from __future__ import annotations

import os
from pathlib import Path


def sync_directory(root: str | Path) -> int:
    """Mirror a HEARTLIGHT vault to Azure Blob Storage.

    Required environment variables:
      HEARTLIGHT_AZURE_CONNECTION_STRING
      HEARTLIGHT_AZURE_CONTAINER
    """
    try:
        from azure.storage.blob import BlobServiceClient
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("Install Azure support with: pip install -e '.[azure]'") from exc

    connection_string = os.environ.get("HEARTLIGHT_AZURE_CONNECTION_STRING")
    container_name = os.environ.get("HEARTLIGHT_AZURE_CONTAINER")
    if not connection_string or not container_name:
        raise RuntimeError(
            "Set HEARTLIGHT_AZURE_CONNECTION_STRING and HEARTLIGHT_AZURE_CONTAINER"
        )

    source_root = Path(root).expanduser().resolve()
    service = BlobServiceClient.from_connection_string(connection_string)
    container = service.get_container_client(container_name)
    try:
        container.create_container()
    except Exception as exc:  # container may already exist
        if exc.__class__.__name__ not in {"ResourceExistsError", "ContainerAlreadyExists"}:
            raise

    uploaded = 0
    for path in sorted(p for p in source_root.rglob("*") if p.is_file()):
        relative = path.relative_to(source_root).as_posix()
        with path.open("rb") as handle:
            container.upload_blob(name=relative, data=handle, overwrite=True)
        uploaded += 1
    return uploaded
