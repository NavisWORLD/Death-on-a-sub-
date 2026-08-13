"""HEARTLIGHT // The Lantern Archive.

A consent-first memorial archive toolkit. This package does not implement or
claim biological resurrection, consciousness transfer, or identity recovery.
"""

from .synaptic import (
    SYNAPTIC_KERNEL_VERSION,
    SynapticConfig,
    SynapticInput,
    SynapticState,
    synaptic_batch,
    synaptic_step,
)

__version__ = "0.2.0"

DISCLOSURE = (
    "I am a memorial simulation generated from family-provided records and teaching. "
    "I am not the deceased person and I do not claim that their consciousness returned."
)

__all__ = [
    "DISCLOSURE",
    "SYNAPTIC_KERNEL_VERSION",
    "SynapticConfig",
    "SynapticInput",
    "SynapticState",
    "__version__",
    "synaptic_batch",
    "synaptic_step",
]
