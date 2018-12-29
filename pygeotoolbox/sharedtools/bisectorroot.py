#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


from math import fabs
import log


def bisection(func, a, b, tolerance):
    # https://www.youtube.com/watch?v=QcuVPbN4_Vk
    xl = a
    xr = b
    c = a
    while (fabs(xl-xr) >= tolerance):
        c = (xl + xr)/2.0
        prod = func(xl) * func(c)
        if prod > tolerance:
            xl = c
        elif prod < tolerance:
            xr = c

    return c


def booleanBisection(func, a, b, tolerance):
    tolerance = float(tolerance)
    left = a
    right = b
    leftValue = func(a)
    rightValue = func(b)
    log.debug("[%f-%f]:[%s-%s]" % (left, right, str(leftValue), str(rightValue)))
    center = (left + right)/2.0
    while (fabs(left-right) >= tolerance):
        center = (left + right)/2.0
        centerValue = func(center)
        log.debug("[%f-%f]:\t[%s-%s]\t%f\t%s" % (left, right, str(leftValue), str(rightValue), center, str(centerValue)))

        if centerValue == leftValue:
            left = center
            leftValue = centerValue
        elif centerValue == rightValue:
            right = center
            rightValue = centerValue

    return center


if __name__ == "__main__":
    if False:
        import matplotlib.pyplot as plt
        import numpy as np


        def valueFunction(x):
            return x ** 3 + 1


        answer = bisection(valueFunction, -5, 5, 1e-8)
        print answer


        x = np.linspace(-5, 5, 100)
        plt.plot(x, valueFunction(x))
        plt.grid()
        plt.savefig("test.png")
        plt.show


    if True:
        def isOK(value):
            return value < 36.0


        x = booleanBisection(isOK, 100, -100, 0.01)
        print x