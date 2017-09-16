import sys
import os

datadir = "gitviz_data"
files = os.listdir(datadir)

cond = lambda x : x.find("master")>0
masterfile = [x for x in files if cond(x)]
rest = [x for x in files if not cond(x)]

# read files
# parse json

# find latest commit b[T] from each branch (compare to input date)
timestamp = sys.argv[1]

# sys calls to compute 
# git diff --shortstat b[T] master[T] and
# git diff --shortstat b[T] (git merge-base b[T] master[T])
# parse and output to a file graphs.json as array:
# each element contains data (t,d1,d2) for one branch
