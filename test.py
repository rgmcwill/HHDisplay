"""
=========================
Simple animation examples
=========================

This example contains two animations. The first is a random walk plot. The
second is an image animation.
"""
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

x = [3,5,7,9,3,9]
x.sort()

plt.plot(range(len(x)), x)

plt.show()