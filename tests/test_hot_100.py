import json
import os

import billboard
from utils import get_test_dir


class TestCurrentHot100:
    """Checks that the ChartData object for the current Hot 100 chart has
    entries and instance variables that are valid and reasonable. Does not test
    whether the data is actually correct.
    """

    def setUp(self):
        self.chart = billboard.ChartData('hot-100')

    def test_date(self):
        assert self.chart.date is not None

    def test_ranks(self):
        ranks = list(entry.rank for entry in self.chart)
        assert ranks == list(range(1, 101))

    def test_entries_validity(self):
        assert len(self.chart) == 100
        for entry in self.chart:
            assert len(entry.title) > 0
            assert len(entry.artist) > 0
            assert 1 <= entry.peakPos <= 100
            assert 0 <= entry.lastPos <= 100
            assert entry.weeks >= 0
            assert 1 <= entry.rank <= 100  # Redundant because of test_ranks
            assert isinstance(entry.isNew, bool)

    def test_json(self):
        assert json.loads(self.chart.json())


class TestHistoricalHot100(TestCurrentHot100):
    """Checks that the ChartData object for a previous week's Hot 100 chart
    has all valid fields, and that its string representation matches what
    is expected.
    """

    def setUp(self):
        self.chart = billboard.ChartData('hot-100', date='2015-11-28')

    def test_date(self):
        assert self.chart.date == '2015-11-28'
        assert self.chart.previousDate == '2015-11-21'

    def test_entries_correctness(self):
        reference_path = os.path.join(get_test_dir(), '2015-11-28-hot-100.txt')
        with open(reference_path) as reference:
            assert str(self.chart) == reference.read()
