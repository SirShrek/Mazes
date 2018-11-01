from PIL import Image
Image.MAX_IMAGE_PIXELS = 1000000000 
import time

image = "E:\\GitHub\\mazesolving\\examples\\tiny.png"
##image = "E:\\GitHub\\mazesolving\\examples\\small.png"
##image = "E:\\GitHub\\mazesolving\\examples\\normal.png"
##image = "E:\\GitHub\\mazesolving\\examples\\braid200.png"
##image = "E:\\GitHub\\mazesolving\\examples\\braid2k.png"
##image = "E:\\GitHub\\mazesolving\\examples\\perfect15k.png"
#image = "E:\\GitHub\\mazesolving\\examples\\p15ktest2.png"

output_file = "E:\\GitHub\\mazesolving\\examples\\Out.png"
startPos = None
endPos = None
completed = False
compass = ["N", "E", "S", "W"]
class pos:

    def __init__(self, position):
        self.pos = position
        self.facing = "S"
        self.route = [[self.pos[0], self.pos[1]]]
                        
    def updatePos(self, newPos):
        self.pos[0] = newPos[0]
        self.pos[1] = newPos[1]
        self.route.append(newPos)

    def getPos(self):
        return self.pos

    def updateFacing(self, direction):
        self.facing = direction

    def getFacing(self):
        return self.facing

    def getRoute(self):
        return self.route

print("Loading Map Images")
t0 = time.time()
im = Image.open(image)
width, height = im.size[0], im.size[1]

data = list(im.getdata(0))

listMap = []
rowList = []
rowCount = 0
for i in data:
    rowCount = len(rowList)
    
    if rowCount < width:
        rowList.append(i)
    rowCount = len(rowList)
   
    if rowCount >= width:
        listMap.append(rowList)
        rowList = []

##for l in listMap:
##    print(l)

idx = 0

for i in listMap[0]:
    if i == 1:
        startPos = idx
        break
    idx += 1
print(startPos)
idx = 0
for i in listMap[-1]:
    if i == 1:
        endPos = idx
        break
    idx += 1
print(endPos)

if startPos is None or endPos is None:
    raise ValueError ("Start or End Could Not Be Found")
t1 = time.time()
total = t1 - t0
print("Time Taken To Load Image:" , total)

print("Starting Maze Solving")
t0 = time.time()
print("Start Time: ", t0)
mazeRunner = pos([0, startPos])


def getPath(currentPosition, mapSlice):
    cp = currentPosition
    #if cp[0] != [0-9] or cp[1] != [0-9]:    print (cp)
    path = [None, None, None, None]
    path[0] = mapSlice[cp[0] -1][cp[1]]
    path[1] = mapSlice[cp[0]][cp[1]+1]
    path[2] = mapSlice[cp[0]+ 1][cp[1]]
    path[3] = mapSlice[cp[0]][cp[1]-1]

    return path

def decideStep(options, currentFacing, runnerCompass):
    cf = currentFacing
    leftTurn = False
    rc = runnerCompass.copy()
    ro = options.copy()
    relDiff = 0
    while rc[1] != cf:
        ro.append(ro.pop(0))
        rc.append(rc.pop(0))
        if relDiff < 2:
            relDiff += 1
        else:
            relDiff -= 1
        #print("RelDiff: ", relDiff)
     #   print(rc[1], cf)
##    print(compass)
##    print(options)
    #print("ro", ro)
    #print("rc", rc)
    rf = rc.index(cf)
    #print(cf, rf)   
    #print (cf, rf, relDiff, rf - relDiff)
    
    if relDiff == 0 : relDiff = 1
    if rf - relDiff < 0: relDiff = 1
    #print (cf, rf, relDiff, rf - relDiff)
    lookLeft = ro[rf - relDiff]
    if lookLeft == 1:
        leftTurn = True
     #   print("TurnLEftTURE")
    if leftTurn is True:
        return rc[rf-relDiff]
        
    if ro[rf] == 1:
        return rc[rf]
    if ro[rf +1] == 1:
        return rc[rf +1]
    if ro[rf +2] == 1:
        return rc[rf +2]
    
        
def direction2Cord(result, currentPos):
    cp = currentPos
    if result == "N":
        return [cp[0] -1, cp[1]]
    elif result == "S":
        return [cp[0] + 1, cp[1]]
    elif result == "W":
        return [cp[0], cp[1] -1]
    elif result == "E":
        return [cp[0], cp[1] +1]
    else:
        print("ERROR")
        return None
        
#wherebeen = []
loopcounter = 0
while not completed:
    #print()
    pathOptions = getPath(mazeRunner.getPos(), listMap)
    #print(pathOptions)
    n = decideStep(pathOptions, mazeRunner.getFacing(), compass)
    #print("n: ", n)
    
    mazeRunner.updatePos(direction2Cord(n, mazeRunner.getPos()))
    mazeRunner.updateFacing(n)
##    print(mazeRunner.getPos(), mazeRunner.getFacing())
    loopcounter += 1
    #print (loopcounter)
    A = mazeRunner.getPos()
    #wherebeen.append(A)
    #print(A)
    #if loopcounter == 50:
    if A == [height -1 , endPos]:
        completed = True
        print("Found The Exit")
t1 = time.time()
print("End Time: ", t1)
total = t1 -t0
print("Time Taken: ", total)
resultpath = mazeRunner.getRoute().copy()
length = len(resultpath)
print("Total Steps: ", length)

print ("Saving Image")
im = im.convert('RGB')
impixels = im.load()

#print(mazeRunner.route)


for i in range(0, length - 1):
    a = resultpath[i]
    b = resultpath[i+1]

    # Blue - red
    r = int((i / length) * 255)
    px = (r, 0, 255 - r)

    if a[0] == b[0]:
        # Ys equal - horizontal line
        for x in range(min(a[1],b[1]), max(a[1],b[1])):
            impixels[x,a[0]] = px
    elif a[1] == b[1]:
        # Xs equal - vertical line
        for y in range(min(a[0],b[0]), max(a[0],b[0]) + 1):
            impixels[a[1],y] = px

im.save(output_file)

#for i in mazeRunner.getRoute(): print(i)
