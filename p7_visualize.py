import json
import re
    
def initialize(width):
    world = []
    for i in range(0,width):
      world.append([])
      for j in range(0,width):
        world[i].append('A')
    return world
    
def strToPair(str):
    tile = re.match(r'^\((\d*),(\d*)\)$',str)
    return int(tile.group(1)),int(tile.group(2)) 
      
def printWorld(world,path):
    for y in range(0,len(world)):
        #print row
        str = ''
        for x in range(0,len(world[y])):
            if (x,y) in path:
              str+=path[(x,y)]
            else: 
              str+=(world[y][x])
        print str
        
def printAllWorlds(world,paths):
    for y in range(0,len(world)):
        #print row
        row = ['']
        while len(row) < len(paths):
            row.append('')
        for x in range(0,len(world[y])):
            for i in range(len(row)):
              if len(paths) > i and (x,y) in paths[i]:
                row[i]+=paths[i][(x,y)]
              else: 
                row[i]+=(world[y][x])
        str = ''
        for r in row:
           str+=r
           str+=' '
        print str

#print state["Call"]['Witnesses']
def buildWorld(state):
  world = []
  paths = []
  sprite = {'wall':'W','altar':'a','trap':'%','gem':'g'}
  for call in state["Call"]:
    for witness in call["Witnesses"]:
        for rule in witness["Value"]:
            arg = re.match(r'(\w*)\((.*)?\)$',rule)
            #print arg.group(1), arg.group(2)
            type, req = arg.group(1), arg.group(2)
            if type == 'param':
              #param = re.match(r'^\(\\\"(.*)\\\",(\d*)\)$',req)
              param = re.match(r'\"(.*)\",(\d*)',req)
              world = initialize(int(param.group(2)))
            if type == 'tile':
              x,y = strToPair(req)
              world[y][x] = '.'
            if type == 'sprite':
              param = re.match(r'(.*),(.*)',req)
              x,y = strToPair(param.group(1))
              world[y][x] = sprite[param.group(2)]
            if type == 'touch':
              param = re.match(r'(.*),(.*)',req)
              x,y = strToPair(param.group(1))
              layer = param.group(2)
              while len(paths) <= int(layer):
                paths.append({})
              paths[int(layer)][(x,y)] = layer
  return world,paths

def loadAndBuild(out):
  result = json.loads(out)
  #print result
  world, paths = buildWorld(result)
  #print paths
  #printWorld(world, {})
  printAllWorlds(world,paths)
#for path in paths:
#  print
#  printWorld(world,path)
