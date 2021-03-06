#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# setup.py
# 
# setup for CSSQC
# ----------------------------------------------------------------
# copyright (c) 2014 - Domen Ipavec
# Distributed under The MIT License, see LICENSE
# ----------------------------------------------------------------

from setuptools import setup, find_packages
from setuptools.command.test import test

class buildPly(test):
    def run(self):
        import csslex, cssyacc
        csslex._build()
        cssyacc._build()
        test.run(self)

setup(
    name='CSSQC',
    
    version='0.2',
    
    packages=['csslex', 'cssyacc', 'cssqc', 'cssqc.rules'],
    
    test_suite='nose.collector',
    
    install_requires=['nose', 'ply'],
    
    entry_points={
        'console_scripts': [
            'cssqc=cssqc:main'
        ]
    },
        
    cmdclass={
        'test': buildPly
    },

    package_data={
        'cssqc': ['defaults.cfg', 'order/*.dat', 'group/*.dat']
    }
)