#!/usr/bin/env python2

from Wrestlers import Abdullah
from lib import util, spw

w = spw.Wrestler(Abdullah)

f = open("exporttest.html", 'w')
f.write(util.actionCard2HTML(w))
f.close()

