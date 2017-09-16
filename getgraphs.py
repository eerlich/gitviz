import sys
import os
import subprocess 
import json
import re
import time

def get_files(datadir):
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
    return [x['commit'] for x in jsob if int(x['timestamp'])<ts ][0]

def utf2ascii(data):
    udata=data.decode("utf-8")
    asciidata=udata.encode("ascii","ignore")

def get_diff(a,b):
    process = subprocess.Popen(["git", "diff", "--shortstat", a, b], stdout=subprocess.PIPE)
    output = process.communicate()[0]

    fc = re.match(".*(\d+) files changed", output)
    i = re.match(".*(\d+) insertions", output)
    d = re.match(".*(\d+) deletions", output)

    inserts = i.group() if i else 0
    deletions = d.group() if d else 0
    out = inserts + deletions

    return out

def get_mergebase(a,b):
    process = subprocess.Popen(["git", "merge-base", a, b], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    return output

def writejson(res,files):
    for k in range(len(res)):
        jsval=json.dumps(res[k])
        with open(files[k]) as f:
            f.write(jsval)

def main():
    datadir = "gitviz_data"

    if(len(sys.argv)>1):
        # assume unix timestamp input
        ts = int(sys.argv[1])
    else:
        ts = time.time()

    (f,mf) = get_files(datadir)
    # parse json from files
    js = [parsefile(x) for x in f]
    mjs = [parsefile(x) for x in mf]

    # find latest commit b[T] from each branch (compare to input date)
    commits=[latestcommit(x,ts) for x in js]
    mastercommit=latestcommit(mjs[0],ts)
    mergebases = [get_mergebase(x,mastercommit) for x in commits]

    cumdiffs = [get_diff(a,b) for (a,b) in zip(commits,mergebases)]
    masterdiffs = [get_diff(a,mastercommit) for a in commits]

    # each element contains data (t,d1,d2) for one branch
    result = [{"timestamp": ts, "cumdiff": a, "masterdiff": b} \
            for (a,b) in zip(cumdiffs,masterdiffs)]

    outfiles=[x[:-5]+"_graph.json" for x in f]

    # output to a file graphs.json
    writejson(result, outfiles)

if __name__ == "__main__":
    main()

