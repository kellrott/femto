#!/usr/bin/env python

import os
import sys
import subprocess
import json
from glob import glob
from collections import Counter

sys.path.append( os.path.join(os.getcwd(), "compilers/python/") )
import femto


def compare(a,b):
    return a == b

def which(file):
    for path in os.environ["PATH"].split(":"):
        p = os.path.join(path, file)
        if os.path.exists(p):
            return p

node_exec = which("node")

if node_exec is None:
    node_exec = which("nodejs")

test_results = []
for f in glob("test/code*.py"):
    print "Testing", f
    with open(f) as handle:
        txt = handle.read()
    fn = femto.convert(txt)
    fn_txt = json.dumps( femto.to_dict(fn) )

    code_path = "test.femto"
    with open(code_path, "w") as handle:
        handle.write(fn_txt)

    input_path = f.replace(".py", ".input")
    output_path = f.replace(".py", ".output")

    cmd = [node_exec, "compilers/js/femto_cmd.js", code_path, input_path ]
    print "Running: %s" % (" ".join(cmd))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        test_results.append("JS exec failed")
    else:
        try:
            out_value = json.loads(stdout)
            print "RESULT: %s" % (out_value)
            with open(output_path) as handle:
                test_value = json.loads(handle.read())
            if not compare(test_value, out_value):
                test_results.append("BadOutput")
            else:
                test_results.append("OK")
            print "OK!!!!"
        except ValueError:
            test_results.append("Output Error")
    print "-=-=-=-=-=-=-"


c = Counter(test_results)
print "\n".join( list( "%s:%s" % (a,b) for a, b in c.items() ))
