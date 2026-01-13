"""
Pytest configuration to avoid Prometheus duplicate metrics errors
"""
import pytest
from prometheus_client import REGISTRY


@pytest.fixture(scope="session", autouse=True)
def cleanup_prometheus_registry():
    """Clean up Prometheus registry before test session"""
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        try:
            REGISTRY.unregister(collector)
        except Exception:
            pass
    yield
    # Cleanup after tests
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        try:
            REGISTRY.unregister(collector)
        except Exception:
            pass