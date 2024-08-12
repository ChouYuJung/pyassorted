from rich import print

from pyassorted.modules.read import read_module_with_dependencies, read_py_module


def test_read_py_module():
    module_path = "pyassorted.asyncio.executor"
    model_param = read_py_module(module_path)
    assert model_param is not None
    assert model_param["module_name"] == module_path
    assert len(model_param["source_code"]) > 0


def test_read_module_with_dependencies():
    module_path = "pyassorted.asyncio.executor"
    model_params = read_module_with_dependencies(module_path)
    assert len(model_params) > 1
    assert any("os" == param["module_name"] for param in model_params)

    model_params = read_module_with_dependencies(
        module_path, filter=lambda x: x.startswith("pyassorted")
    )
    assert len(model_params) > 1
    assert all(param["module_name"].startswith("pyassorted") for param in model_params)
