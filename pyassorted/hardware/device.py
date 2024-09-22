import logging
from typing import Literal, Optional, Text

# Support dtype
cpu_supported_dtype = ("float32", "float64")
mps_supported_dtype = ("float16", "float32", "float64", "bfloat16")


def validate_device(
    device: Optional[Text] = None, *, logger: Optional[logging.Logger] = None
) -> Literal["auto", "cpu", "cuda", "mps"]:
    if device is not None and device.strip().lower() == "auto":
        return "auto"

    if device is not None and device.strip().lower() == "cpu":
        return "cpu"

    try:
        import torch  # type: ignore
    except ImportError:
        if logger is not None:
            logger.warning("Torch is not installed. The device will be CPU.")
        return "cpu"

    # Try to find the device
    if device is None:
        if torch.cuda.is_available():
            if logger is not None:
                logger.debug("Device found: CUDA")
            return "cuda"

        elif torch.backends.mps.is_available():
            if logger is not None:
                logger.debug("Device found: MPS")
            return "mps"

        else:
            if logger is not None:
                logger.debug("Device found: CPU")
            return "cpu"

    # Validate cuda device
    if device.strip().startswith("cuda"):
        if not torch.cuda.is_available():
            if logger is not None:
                logger.warning("CUDA is not available. The device will be CPU.")
            return "cpu"
        return "cuda"

    # Validate mps device
    if device.strip().startswith("mps"):
        if not torch.backends.mps.is_available():
            if logger is not None:
                logger.warning("MPS is not available. The device will be CPU.")
            return "cpu"
        return "mps"

    # Validate cpu device
    if device.strip() == "cpu":
        return "cpu"
    # Validate unknown device
    if logger is not None:
        logger.warning(f"Unknown device: {device}. The device will be CPU.")
    return "cpu"


def validate_dtype(
    device: Literal["auto", "cpu", "cuda", "mps"],
    dtype: Optional[Text] = None,
    *,
    logger: Optional[logging.Logger] = None,
):
    if dtype is None:
        return
    device_str_value = device.strip().lower()
    dtype_value = dtype.strip().lower()

    if device_str_value == "cpu":
        if dtype_value not in cpu_supported_dtype:
            if logger is not None:
                logger.warning(f"Invalid dtype for CPU: {dtype}")
            return
    elif device_str_value.startswith("mps"):
        if dtype_value not in mps_supported_dtype:
            if logger is not None:
                logger.warning(f"Invalid dtype for MPS: {dtype}")
            return
    elif device_str_value.startswith("auto"):
        return
    elif device_str_value.startswith("cuda"):
        return
    else:
        if logger is not None:
            logger.debug(f"Unhandled device and dtype yet: {device} {dtype}.")
