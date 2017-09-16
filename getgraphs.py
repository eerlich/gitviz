import sys
import os
import json
import time

def get_files(datadir = "gitviz_data"):
    files = os.listdir(datadir)
    files = [os.path.join(datadir, x) for x in files]

    cond = lambda x : x.find("master")>0
    masterfile = [x for x in files if cond(x)]
    rest = [x for x in files if not cond(x)]

    return (rest,masterfile)

def parsefile(f):
    with open(f) as data:
        out=json.load(data)
    return out

def latestcommit(jsob,ts):
    [x['commit'] for x in jsob if int(x['timestamp'])<ts ][0]

def main():
    if(len(sys.argv)>1):
        # assume unix timestamp input
        ts = int(sys.argv[1])
    else:
        ts = time.time()

    (f,mf) = get_files()
    # parse json from files
    js = [parsefile(x) for x in f]
    mjs = [parsefile(x) for x in mf]

    # find latest commit b[T] from each branch (compare to input date)
    commits=[latestcommit(x,ts) for x in js]
    mastercommit=latestcommit(mjs[0],ts)

    # sys calls to compute 

    # git diff --shortstat b[T] master[T] and
    # git diff --shortstat b[T] (git merge-base b[T] master[T])
    # parse and output to a file graphs.json as array:
    # each element contains data (t,d1,d2) for one branch

if __name__ == "__main__":
    main()

