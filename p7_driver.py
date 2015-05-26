import subprocess
import json
import collections
import random
import sys
import p7_visualize

def solve(*args):
  GRINGO = "./gringo"
  REIFY = "./reify"
  CLINGO = "./clingo"
  gringo = subprocess.Popen(
    [GRINGO, "level-core.lp","level-style.lp","level-sim.lp","level-shortcuts.lp"],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE)
  reify = subprocess.Popen([REIFY],
    stdin = gringo.stdout,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE)
  clingo = subprocess.Popen([CLINGO, "-","meta.lp","metaD.lp","metaO.lp","metaS.lp","-c","width=10","--parallel-mode=4","--outf=2", "--sign-def=3","--seed="+str(random.randint(0,1<<30))],
    stdin = reify.stdout,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE)
  out, err = clingo.communicate()
  if err:
    print err
  return p7_visualize.loadAndBuild(out)
solve()
