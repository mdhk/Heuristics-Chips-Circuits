"""
Basic configuration.
This was created because different modules needed basic information such as
WIDTH, HEIGHT etc. without hard-coding this into each module.
"""

from data.config1 import width as WIDTH, height as HEIGHT, gates
from data.netlist import netlist_2 as netlist
from algorithms import aStar as findPath

DEPTH = 8
SURF = WIDTH * HEIGHT
