from pyassorted.hardware.device import validate_device, validate_dtype


def test_validate_device():
    assert validate_device("auto") == "auto"
    assert validate_device("cpu") == "cpu"
    assert validate_device("cuda") in ["cuda", "cpu"]  # Depends on CUDA availability
    assert validate_device("mps") in ["mps", "cpu"]  # Depends on MPS availability
    assert validate_device("unknown_device") == "cpu"


def test_validate_dtype():
    assert validate_dtype("cpu", "float32") is None
    assert validate_dtype("cpu", "float64") is None
    assert validate_dtype("cpu", "int32") is None  # Invalid dtype for CPU
    assert validate_dtype("mps", "float16") is None
    assert validate_dtype("mps", "float32") is None
    assert validate_dtype("mps", "int32") is None  # Invalid dtype for MPS
    assert validate_dtype("cuda", "float32") is None
    assert validate_dtype("auto", "float32") is None
