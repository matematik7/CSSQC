#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# cssqc/singleLinePerSelector.py
# 
# Do not allow selector on multiple lines.
# ----------------------------------------------------------------
# copyright (c) 2014 - Domen Ipavec
# Distributed under The MIT License, see LICENSE
# ----------------------------------------------------------------

from cssqc.qualityWarning import QualityWarning
from cssyacc import Whitespace
from cssqc.helpers import inspectWhitespaces

import re

def getHelp():
    return """Do not allow selector over multiple lines."""

class singleLinePerSelector:
    def __init__(self, data):
        pass

    def on_Selector(self, s):
        warnings = []
        for i in range(len(s.text)):
            if i == 0 \
                and type(s.text[i]) is Whitespace:
                continue
            if i == len(s.text) - 1 \
                and type(s.text[i]) is Whitespace:
                continue
            ln = inspectWhitespaces(s.text[i], lambda ws: '\n' not in ws.value)
            if ln != -1:
                warnings.append(QualityWarning('singleLinePerSelector', ln, \
                    'Selector over multiple lines.'))
        return warnings