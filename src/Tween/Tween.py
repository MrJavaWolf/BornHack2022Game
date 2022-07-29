#!/usr/bin/python
# -*- coding: utf-8 -*-
# Src: https://github.com/Polynominal/PyFlax

import math


def linear(x: float):
    return x
def quad(x: float):
    return x * x
def quadout(x: float):
    return 1 - quad(x)
def cubic(x: float):
    return x * x * x
def cubicout(x: float):
    return 1 - cubic(x)
def quint(x: float):
    return x * x * x * x
def quintout(x: float):
    return 1 - quint(x)
def sine(x: float):
    return -math.cos(x * (math.pi * .5)) + 1
def sineout(x: float):
    return 1 - sine(x)
def cosine(x: float):
    return -math.sine(x * (math.pi * .5)) + 1
def cosineout(x: float):
    return 1 - cosine(x)
