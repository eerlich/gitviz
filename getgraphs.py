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

    inserts = int(i.group(1)) if i else 0
    deletions = int(d.group(1)) if d else 0

    out = inserts + deletions

    return out

def get_mergebase(a,b):
    process = subprocess.Popen(["git", "merge-base", a, b], stdout=subprocess.PIPE)
    output = process.communicate()[0]

    return output.strip()

def writejson(res,files):
    for k in range(len(res)):
        jsval=json.dumps(res[k])
        with open(files[k], "w") as f:
            f.write(jsval)

def run(timestamps):
    datadir = "gitviz_data"
    outdir = "gitviz_out"

    (f,mf) = get_files(datadir)
    # parse json from files
    js = [parsefile(x) for x in f]
    mjs = [parsefile(x) for x in mf]

    res = []

    for ts in timestamps:
        # find latest commit b[T] from each branch (compare to input date)
        commits=[latestcommit(x,ts) for x in js]
        mastercommit=latestcommit(mjs[0],ts)
        mergebases = [get_mergebase(x,mastercommit) for x in commits]

        cumdiffs = [get_diff(a,b) for (a,b) in zip(commits,mergebases)]
        masterdiffs = [get_diff(a,mastercommit) for a in commits]

        # each element contains data (t,d1,d2) for one branch
        res += [[{"timestamp": ts, "cumdiff": a, "masterdiff": b} \
                for (a,b) in zip(cumdiffs,masterdiffs)]]

    # transpose results 
    results=map(list,map(None,*res))

    outfiles=[os.path.split(x)[1][:-5]+"_graph.json" for x in f]
    writejson(results, outfiles)

def main():
    if(len(sys.argv) > 1):
        # number of datapoints to generate (30 minute intervals)
        N = int(sys.argv[1])
        t=int(time.time())
        interval=15*60 # in seconds 
        ts = [t-interval*k for k in range(N)]
    else:
        ts = [int(time.time())]

    run(ts)

if __name__ == "__main__":
    main()

