from itertools import chain, repeat
import json
import os
import re
import unittest
import datetime

import billboard


class CurrentHot100Test(unittest.TestCase):
    """Checks that the ChartData object for the current Hot 100 chart
    has all valid fields, and that its entries also have valid fields.
    """

    def setUp(self):
        self.chart = billboard.ChartData('hot-100')

    def test_correct_fields(self):
        assert self.chart.date is not None
        assert list(sorted(entry.rank for entry in self.chart)
                    ) == list(range(1, 101))

    def test_valid_entries(self):
        assert len(self.chart) == 100
        for entry in self.chart:
            assert len(entry.title) > 0
            assert len(entry.artist) > 0
            assert entry.peakPos >= 1 \
                and entry.peakPos <= 100
            assert entry.lastPos >= 0 \
                and entry.lastPos <= 100  # 0 means new entry
            assert entry.weeks >= 0
            assert entry.rank >= 1 \
                and entry.rank <= 100
            assert repr(entry)

    def test_valid_json(self):
        assert json.loads(self.chart.json())


class HistoricalHot100Test(CurrentHot100Test):
    """Checks that the ChartData object for a previous week's Hot 100 chart
    has all valid fields, and that its string representation matches what
    is expected.
    """

    def setUp(self):
        self.chart = billboard.ChartData('hot-100', date='2015-11-28')

    def test_correct_fields(self):
        assert self.chart.date == '2015-11-28'
        assert self.chart.previousDate == '2015-11-21'

    def test_correct_entries(self):
        reference_path = os.path.join(get_test_dir(), '2015-11-28-hot-100.txt')
        with open(reference_path) as reference:
            assert str(self.chart) == reference.read()


class CurrentArtist100Test(unittest.TestCase):
    """Checks that the ChartData object for the current Artist 100 chart
    has all valid fields, and that its entries also have valid fields.
    """

    def setUp(self):
        self.chart = billboard.ChartData('artist-100')

    def test_correct_fields(self):
        assert self.chart.date is not None
        assert list(sorted(entry.rank for entry in self.chart)
                    ) == list(range(1, 101))

    def test_valid_entries(self):
        assert len(self.chart) == 100
        for entry in self.chart:
            assert len(entry.title) == 0  # No titles for this chart
            assert len(entry.artist) > 0
            assert entry.peakPos >= 1 \
                and entry.peakPos <= 100
            assert entry.lastPos >= 0 \
                and entry.lastPos <= 100  # 0 means new entry
            assert entry.weeks >= 0
            assert entry.rank >= 1 \
                and entry.rank <= 100
            assert repr(entry)

    def test_valid_json(self):
        assert json.loads(self.chart.json())


class HistoricalArtist100Test(CurrentArtist100Test):
    """Checks that the ChartData object for a previous week's Artist 100 chart
    has all valid fields, and that its string representation matches what
    is expected.
    """

    def setUp(self):
        self.chart = billboard.ChartData('artist-100', date='2014-07-26')

    def test_correct_fields(self):
        assert self.chart.date == '2014-07-26'
        assert self.chart.previousDate == '2014-07-19'

    def test_correct_entries(self):
        reference_path = os.path.join(get_test_dir(),
                                      '2014-07-26-artist-100.txt')
        with open(reference_path) as reference:
            assert str(self.chart) == reference.read()


class DateRoundingTest(unittest.TestCase):
    """Checks that the Billboard website is rounding dates correctly: it should
    round up to the nearest date on which a chart was published.
    """

    def setUp(self):
        self.chart = billboard.ChartData('hot-100', date='1000-10-10')

    def test_correct_fields(self):
        assert self.chart.date == '1958-08-04'  # The first Hot 100 chart


class CurrentGreatestHot100SinglesTest(unittest.TestCase):
    """Checks that the ChartData object for the current
    greatest-hot-100-singles chart has all valid fields, and that its entries
    also have valid fields.

    The greatest-hot-100-singles chart is special in that it does not provide
    peak/last position or weeks-on-chart data.
    """

    def setUp(self):
        self.chart = billboard.ChartData('greatest-hot-100-singles')

    def test_correct_fields(self):
        assert self.chart.date is None
        assert list(sorted(entry.rank for entry in self.chart)
                    ) == list(range(1, 101))

    def test_valid_entries(self):
        assert len(self.chart) == 100
        for entry in self.chart:
            assert len(entry.title) > 0
            assert len(entry.artist) > 0
            assert entry.peakPos is None
            assert entry.lastPos is None
            assert entry.weeks is None
            assert entry.rank >= 1 \
                and entry.rank <= 100
            assert repr(entry)

    def test_valid_json(self):
        assert json.loads(self.chart.json())


class DatetimeTest(unittest.TestCase):
    """Checks that ChartData correctly handles datetime objects as the
    date parameter.
    """

    def setUp(self):
        self.chart = billboard.ChartData('hot-100', datetime.date(2016, 7, 8))

    def test_successful_load(self):
        self.assertTrue(len(self.chart) > 0)


def get_test_dir():
    """Returns the name of the directory containing this test file.
    """
    return os.path.dirname(os.path.realpath(__file__))
