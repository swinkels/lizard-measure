#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

import logging

from lizard_esf.models import get_data_main_esf
from lizard_measure.pattern_matcher import PatternMatcher
from lizard_measure.pattern_measures_retriever import PatternMeasuresRetriever

logger = logging.getLogger(__name__)


class SuitableMeasureInfo(object):

    def __init__(self, measure, is_country_wide):
        self.measure = measure
        self.is_country_wide = is_country_wide


class SuitableMeasureInfoFactory(object):

    def create(self, esf_pattern, measures):
        return [SuitableMeasureInfo(m, esf_pattern.data_set is None) for m in measures]


class SuitableMeasures(object):
    """Implements the retrieval of the suitable measures of an area."""

    def __init__(self, suitable_measure_info_factory, pattern_measures_retriever,
        pattern_matcher):
        self.suitable_measure_info_factory = suitable_measure_info_factory
        self.pattern_measures_retriever = pattern_measures_retriever
        self.pattern_matcher = pattern_matcher

    def get(self, area):
        """Return the list of suitable measures for the given area."""
        suitable_measures = []
        area_pattern = self._get_area_pattern(area)
        measures_dict = self.pattern_measures_retriever.retrieve(area)
        for esf_pattern, measures in measures_dict.items():
            if self.pattern_matcher.matches(area_pattern, esf_pattern.pattern):
                suitable_measures += self.suitable_measure_info_factory.create(esf_pattern, measures)
        return suitable_measures

    def _get_area_pattern(self, area):
        """Return the string that specifies the critical ESFs of the given area."""
        result = ''
        esf_data = get_data_main_esf(area)
        for e in esf_data:
            if e['judgment'] == 'critical':
                result += 'X'
            else:
                result += '-'
        return result


def get_suitable_measures(area):
    """Return the list of suitable measures for the given area."""
    measures = SuitableMeasures(SuitableMeasureInfoFactory(),
                                PatternMeasuresRetriever(),
                                PatternMatcher())
    return measures.get(area)
