#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# cssqc/noTagWithClass.py
# 
# Do not allow tag with class (e.g. div.class)
# ----------------------------------------------------------------
# copyright (c) 2014 - Domen Ipavec
# Distributed under The MIT License, see LICENSE
# ----------------------------------------------------------------

from cssqc.qualityWarning import QualityWarning
from csslex import t_IDENT
from cssyacc import Whitespace, Comment
from cssqc.helpers import isTupleWithValue

import re

def getHelp():
    return """Do not allow tag with class (e.g. div.class)."""

class noTagWithClass:
    def __init__(self, data):
        self.ident_re = re.compile(t_IDENT)

    def on_Selector(self, s):
        warnings = []
        for i in range(1,len(s.text)-1):
            try:
                class_name = s.text[i+1][0]
                tag_name = s.text[i-1][0]
                if isTupleWithValue(s.text[i], '.') \
                    and self.ident_re.match(class_name) \
                    and self.ident_re.match(tag_name) \
                    and (i-1 == 0 \
                        or type(s.text[i-2]) is Whitespace):
                    warnings.append(QualityWarning('noTagWithClass', s.text[i][1], 'Tag with class: ' + tag_name + '.' + class_name))
            except:
                pass
        return warnings
