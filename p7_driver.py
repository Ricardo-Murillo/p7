import subprocess
import json
import collections
import random
import sys
import p7_visualize

def solve(*args):
  CLINGO = "./clingo"
  clingo = subprocess.Popen(
    [CLINGO, "--outf=2"] + list(args),
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE)
  out, err = clingo.communicate()
  if err:
    print err
  return p7_visualize.loadAndBuild(out)
 
def solve_randomly(*args):
    """Like solve() but uses a random sign heuristic with a random seed."""
    args = list(args) + ["--sign-def=3","--seed="+str(random.randint(0,1<<30))]
    return solve(*args) 
    
solve_randomly("level-core.lp","-c","width=10")
