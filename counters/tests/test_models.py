from model_bakery import baker

from counters.models import Counter, CounterType


def test_simple_prepares(db):
    baker.prepare(Counter)
    baker.prepare(CounterType)


def test_make_count_manager(db, lozenge_counter):
    c1 = Counter.objects.make_count(type_obj=lozenge_counter)
    c2 = Counter.objects.make_count(type_obj=lozenge_counter, count=3)

    counts = Counter.objects.all()
    assert len(counts) == 2
