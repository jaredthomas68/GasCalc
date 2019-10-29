#!/usr/bin/env python
# encoding: utf-8

from numpy.distutils.core import setup, Extension

setup(
    name='GasCalc',
    version='0.0.0',
    description='Compressible gas calculation equations',
    package_dir={'': 'src'},
    packages=['gas_calc'],
    license='Apache License, Version 2.0',
)

