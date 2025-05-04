import pytest
import os

@pytest.fixture(autouse=True)
def set_test_env():
    """Set environment variables for testing"""
    # Skip model downloads unless explicitly testing them
    os.environ["SKIP_MODEL_TESTS"] = "1"
    
    yield
    
    # Clean up
    if "SKIP_MODEL_TESTS" in os.environ:
        del os.environ["SKIP_MODEL_TESTS"]