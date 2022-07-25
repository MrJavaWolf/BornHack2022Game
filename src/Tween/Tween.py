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


ease = {
    'linear': linear,
    'quad': quad,
    'quad-out': quadout,
    'cubic': cubic,
    'cubic-out': cubicout,
    'quint': quint,
    'quint-out': quintout,
    'sine': sine,
    'sine-out': sineout,
    'cosine': cosine,
    'cosine-out': cosineout,
    }


def findDistance(x, y):
    if not x or not y:
        return 0
    else:
        return max(x, y) - min(x, y)


class single:

    def __init__(
        self,
        time,
        item,
        exp,
        mode='linear'):
        self.progress = 0
        self.rate = time > 0 and 1 / time or 0
        self.start = item
        self.current = item
        self.diff = exp - item
        self.mode = mode
        self.exp = exp
        self.done = False
        self.delay = 0
        self.initt = 0

    def get(self):
        return self.current

    def update(self, dt):
        self.progress = self.progress + self.rate * dt
        p = self.progress
        x = p >= 1 and 1 or ease[self.mode](p)
        self.current = self.start + x * self.diff
        if p > 1:
            self.done = True


class _to:

    def __init__(
        self,
        time,
        obj,
        var,
        parent,
        mode='Linear',
        done=None):
        self.tweens = []
        self.var = var
        self.obj = obj
        self.done = False
        self.onComplete = done
        self.initt = 0
        self.parent = parent
        self.delay = 0
        self._after = None
        # key val

        for (i, v) in var.items():
            if type(v) == int:
                item = single(time, getattr(obj, i), v)
                list.insert(self.tweens, len(self.tweens) + 1, item)
            elif type(v) == list:
                t = getattr(obj, i)
                if type(v) == list:
                    items = v
                    no = 0
                    for var in v:
                        item = single(time, getattr(t[no]), var)
                        list.insert(self.tweens, len(self.tweens) + 1, item)
                        no += 1
            else:
                print('The item: ' + v + ' for ' + i + ' is not a number or a list!')

    def update(self, dt):
        if self.initt > self.delay:
            no = 0
            items = []
            for (i, v) in self.var.items():
                self.tweens[no].update(dt)
                setattr(self.obj, i, self.tweens[no].get())
                if self.tweens[no].done:
                    items.insert(len(items) + 1, i)
                no = no + 1
            no = 0
            for item in self.tweens:
                if item.done:
                    self.tweens.remove(item)
                no = no + 1
            for item in items:
                self.var.pop(item, None)
            if len(self.tweens) == 0:
                self.done = True
                if self._after:
                    self = self._after(self)
                else:
                    if self.onComplete:
                        self.onComplete()
        else:
            self.initt += dt
        pass

    def after(self, time, var, mode='linear'):
        self._after = _to(
            time,
            self.obj,
            var,
            mode,
            False,
            self.parent)
        list.insert(self.parent.tweens, len(self.parent.tweens) + 1, self._after)
        return self._after

    def set_delay(self, t):
        self.delay = t

    def stop(self):
        list.remove(self.parent.tweens, self)
        pass


class Tween:

    def __init__(self):
        self.tweens = []
        pass

    # VAR HAS TO BE DICT WITH STR:EXPVAL
    def to(self,
        time,
        obj,
        var,
        mode='Linear',
        func=None):
        mode = mode or 'linear'
        t = _to(
            time,
            obj,
            var,
            mode,
            func,
            self,
            )
        list.insert(self.tweens, len(self.tweens) + 1, t)
        return

    def update(self, dt):
        for tween in self.tweens:
            tween.update(dt)
            if tween.done:
                self.tweens.remove(tween)
        pass
