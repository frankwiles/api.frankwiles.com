import pytest

from model_bakery import baker


@pytest.fixture
def lozenge_counter(db):
    return baker.make("counters.CounterType", name="Lozenge", slug="lozenge")
