#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# cssqc/noRedundantChildSelectors.py
# 
# Do not allow redundant child selectors.
# (e.g. ul.class li is ok, but ul li {} is not)
# ----------------------------------------------------------------
# copyright (c) 2014 - Domen Ipavec
# Distributed under The MIT License, see LICENSE
# ----------------------------------------------------------------

from cssqc.qualityWarning import QualityWarning
from cssyacc import Whitespace
from cssqc.helpers import isTupleWithValues, isLast, isTupleWithValue

def getHelp():
    return """Do not allow redundant child selectors (e.g. ul.class li is ok, but ul li {} is not)."""

class noRedundantChildSelectors:
    def __init__(self, data):
        self.redundancies = (
            ('table', ('tr', 'th', 'td')),
            ('ul', ('li',)),
            ('ol', ('li',)),
            ('select', ('option',))
        )

    def isChild(self, i, l):
        return i != 0 \
            and (isTupleWithValue(l[i-1], '>') \
                or (type(l[i-1]) is Whitespace \
                    and i - 1 != 0 \
                    and isTupleWithValue(l[i-2], '>')))

    def hasDescendants(self, i, l, descendants):
        return not isLast(i, l) \
            and type(l[i+1]) is Whitespace \
            and not isLast(i+1, l) \
            and isTupleWithValues(l[i+2], descendants)

    def hasChildren(self, i, l, children):
        if isLast(i, l):
            return False
        if type(l[i+1]) is Whitespace:
            i += 1
        if isLast(i, l) or not isTupleWithValue(l[i+1], '>'):
            return False
        if isLast(i+1, l):
            return False
        if type(l[i+2]) is Whitespace:
            i += 1
        if isLast(i+1, l) or not isTupleWithValues(l[i+2], children):
            return False
        return True

    def on_Selector(self, s):
        warnings = []
        for i in range(len(s.text)):
            for parent, children in self.redundancies:
                if isTupleWithValue(s.text[i], parent) \
                    and (self.hasDescendants(i, s.text, children) \
                        or self.hasChildren(i, s.text, children)) \
                    and not self.isChild(i, s.text):
                        warnings.append(QualityWarning('noRedundantChildSelectors', s.text[i][1], 'Redundant child selector for %s.' % parent))
        return warnings
