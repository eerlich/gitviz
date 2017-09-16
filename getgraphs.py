import sys
import os

datadir = "gitviz_data"
files = os.listdir(datadir)
cond = lambda x : x.find("master")>0

masterfile = [x for x in files if cond(x)]
rest = [x for x in files if not cond(x)]



