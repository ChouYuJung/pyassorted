import numpy as np
import pytest

from pyassorted.numerals.calculation import mean_pooling


@pytest.mark.parametrize("dtype", [np.float16, np.float32, np.float64])
def test_mean_pooling(dtype):
    # Test case 1: Basic functionality
    last_hidden_states = np.array([[[1, 2], [3, 4], [5, 6]]], dtype=dtype)
    attention_mask = np.array([[1, 1, 1]], dtype=dtype)
    expected_output = np.array([[3, 4]], dtype=dtype)

    result = mean_pooling(last_hidden_states, attention_mask)
    np.testing.assert_allclose(result, expected_output, rtol=1e-5)

    # Test case 2: Masked values
    last_hidden_states = np.array([[[1, 2], [3, 4], [5, 6]]], dtype=dtype)
    attention_mask = np.array([[1, 1, 0]], dtype=dtype)
    expected_output = np.array([[2, 3]], dtype=dtype)

    result = mean_pooling(last_hidden_states, attention_mask)
    np.testing.assert_allclose(result, expected_output, rtol=1e-5)

    # Test case 3: Multiple batches
    last_hidden_states = np.array(
        [[[1, 2], [3, 4], [5, 6]], [[7, 8], [9, 10], [11, 12]]], dtype=dtype
    )
    attention_mask = np.array([[1, 1, 1], [1, 0, 0]], dtype=dtype)
    expected_output = np.array([[3, 4], [7, 8]], dtype=dtype)

    result = mean_pooling(last_hidden_states, attention_mask)
    np.testing.assert_allclose(result, expected_output, rtol=1e-5)


def test_mean_pooling_edge_cases():
    # Test case 4: All masked
    last_hidden_states = np.array([[[1, 2], [3, 4]]], dtype=np.float32)
    attention_mask = np.array([[0, 0]], dtype=np.float32)
    expected_output = np.array([[0, 0]], dtype=np.float32)

    result = mean_pooling(last_hidden_states, attention_mask)
    np.testing.assert_allclose(result, expected_output, rtol=1e-5)

    # Test case 5: Empty input
    last_hidden_states = np.array([], dtype=np.float32).reshape(0, 0, 2)
    attention_mask = np.array([], dtype=np.float32).reshape(0, 0)
    expected_output = np.array([], dtype=np.float32).reshape(0, 2)

    result = mean_pooling(last_hidden_states, attention_mask)
    np.testing.assert_array_equal(result, expected_output)


def test_mean_pooling_input_validation():
    # Test case 6: Mismatched shapes
    last_hidden_states = np.array([[[1, 2], [3, 4]]], dtype=np.float32)
    attention_mask = np.array([[1, 1, 1]], dtype=np.float32)

    with pytest.raises(ValueError):
        mean_pooling(last_hidden_states, attention_mask)

    # Test case 7: Wrong number of dimensions
    last_hidden_states = np.array([[1, 2], [3, 4]], dtype=np.float32)
    attention_mask = np.array([1, 1], dtype=np.float32)

    with pytest.raises(ValueError):
        mean_pooling(last_hidden_states, attention_mask)
