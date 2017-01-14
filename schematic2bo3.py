from nbt import *
import os
import math
import bo3template
from tkinter.filedialog import askopenfilename

# Grab file location
location = ''
while True:
        location = askopenfilename()
        location = location.replace('/', os.sep)
        #location = input('Enter full file path: ')
        if os.path.isfile(location):
                if not location.endswith('.schematic'):
                        print('That is not a .schematic file :I')
                        location = ''
                else:
                        break
        elif os.path.isdir(location):
                print('That is a directory, not a file :I')
        else:
                print('That is not even a file :I')
name = location[location.rfind(os.sep)+1:location.find('.schematic')]


# Create output directory
outlocation = location[:location.rfind('.')] + '-bo3'
if not os.path.isdir(outlocation):
        os.mkdir(outlocation)

# Open file as nbt
schematic = nbt.NBTFile(location)

# Set variables from nbt
height = int(schematic['Height'].value)
length = int(schematic['Length'].value)
width = int(schematic['Width'].value)
blocks = schematic['Blocks']
data = schematic['Data']
tileent = schematic['TileEntities']
tiletemp = ['54', '52', '138', '137']
bbchest = True

# Make sure schematic is small enough
assert length <= 160 and width <= 160, name + ".schematic is too large to convert to bo3. bo3 files can only handle structure dimensions up to 160x160 blocks (10x10 chunks)"

# Create nbt files from schematic
# Create folders first
nbtlocation = outlocation + os.sep + 'nbt'
if not os.path.isdir(nbtlocation):
        os.mkdir(nbtlocation)
chestlocation = nbtlocation + os.sep + 'Chests'
if not os.path.isdir(chestlocation):
        os.mkdir(chestlocation)
spawnerlocation = nbtlocation + os.sep + 'Spawner'
if not os.path.isdir(spawnerlocation):
        os.mkdir(spawnerlocation)
misclocation = nbtlocation + os.sep + 'Misc'
if not os.path.isdir(misclocation):
        os.mkdir(misclocation)
# Cycle through tile entities and create nbt files and lists
if tileent:
        print("Creating nbt files...")
chests = []
spawners = []
misc = []
for ent in tileent:
        if str(ent['id']) == 'minecraft:chest':
                chests.append(nbt.NBTFile())
                i = len(chests)-1
                chests[i].name = name + "-Chest" + str(i+1)
                chests[i].tags.append(ent['Items'])
                chests[i].tags.append(ent['id'])
                chests[i].write_file(chestlocation+os.sep+chests[i].name+".nbt")
                chests[i].tags.append(ent['x'])
                chests[i].tags.append(ent['y'])
                chests[i].tags.append(ent['z'])
        elif str(ent['id']) == 'minecraft:mob_spawner':
                spawners.append(nbt.NBTFile())
                i = len(spawners)-1
                spawners[i].name = name + "-Spawner" + str(i+1)
                spawners[i].tags.append(ent['SpawnData'])
                spawners[i].tags.append(ent['SpawnPotentials'])
                spawners[i].tags.append(ent['Delay'])
                spawners[i].tags.append(ent['id'])
                spawners[i].tags.append(ent['MaxNearbyEntities'])
                spawners[i].tags.append(ent['MaxSpawnDelay'])
                spawners[i].tags.append(ent['MinSpawnDelay'])
                spawners[i].tags.append(ent['RequiredPlayerRange'])
                spawners[i].tags.append(ent['SpawnCount'])
                spawners[i].tags.append(ent['SpawnRange'])
                spawners[i].write_file(spawnerlocation+os.sep+spawners[i].name+".nbt")
                spawners[i].tags.append(ent['x'])
                spawners[i].tags.append(ent['y'])
                spawners[i].tags.append(ent['z'])
        else:
                misc.append(nbt.NBTFile())
                i = len(misc)-1
                misc[i].tags.append(ent['id'])
                if str(ent['id']) == 'minecraft:command_block':
                        misc[i].name = name + "-CommandBlock" +str(i+1)
                elif str(ent['id']) == 'minecraft:beacon':
                        misc[i].name = name + "-Beacon" +str(i+1)
                        misc[i].tags.append(ent['Levels'])
                        misc[i].tags.append(ent['Lock'])
                        misc[i].tags.append(ent['Primary'])
                        misc[i].tags.append(ent['Secondary'])
                misc[i].write_file(misclocation+os.sep+misc[i].name+".nbt")
                misc[i].tags.append(ent['x'])
                misc[i].tags.append(ent['y'])
                misc[i].tags.append(ent['z'])

                
# Create bo3
# Create arrays of bo3 outfiles if bigger than chunk
if length > 16 or width > 16:
        print('Creating bo3 files...')
        outfile = []
        for i in range(math.ceil(width/16)):
                outfile.append([])
                for j in range(math.ceil(length/16)):
                        # Create file
                        outfile[i].append(open(outlocation+os.sep+name+'-C'+str(i)+'R'+str(j)+'.bo3', 'w'))
                        # Write top half of template
                        for line in bo3template.top():
                                outfile[i][j].write(line)
# Or just make a single one if it fits within a chunk                        
else:
        print('Creating b03 file...')
        outfile = open(outlocation+os.sep+name+'.bo3', 'w')
        for line in bo3template.top():
                outfile.write(line)

# Block conversion
for x in range(width):
        for z in range(length):
                for y in range(height):
                        i = (y*length+z)*width+x
                        mcid = str(blocks[i])
                        if mcid in tiletemp:
                                line = "RandomBlock("
                                if mcid == '54':
                                        mcid = "CHEST,../../nbt/Chests/"
                                        print(str(x)+':'+str(y)+":"+str(z))
                                        for j in range(len(chests)):
                                                if x == chests[j]['x'].value and z == chests[j]['z'].value and y == chests[j]['y'].value:
                                                        if bbchest:
                                                                if chests[j]['Items'].__len__() == 1:
                                                                        if str(chests[j]['Items'][0]['id']) == 'minecraft:iron_block':
                                                                                mcid = 'CHEST,../../nbt/Chests/Common1.nbt,25,CHEST,../../nbt/Chests/Common2.nbt,25,CHEST,../../nbt/Chests/Common3.nbt,25,CHEST,../../nbt/Chests/Common4.nbt,25,CHEST,../../nbt/Chests/Common5.nbt,25,CHEST,../../nbt/Chests/Common6.nbt,25,CHEST,../../nbt/Chests/Common7.nbt,25,CHEST,../../nbt/Chests/Common8.nbt,25,CHEST,../../nbt/Chests/Common9.nbt,25,CHEST,../../nbt/Chests/Common10.nbt,25,CHEST,../../nbt/Chests/Common11.nbt,25,CHEST,../../nbt/Chests/Common12.nbt,25,CHEST,../../nbt/Chests/Common13.nbt,25,CHEST,../../nbt/Chests/Common14.nbt,25,CHEST,../../nbt/Chests/Common15.nbt,100'
                                                                        elif str(chests[j]['Items'][0]['id']) == 'minecraft:gold_block':
                                                                                mcid = 'CHEST,../../nbt/Chests/Rare1.nbt,25,CHEST,../../nbt/Chests/Rare2.nbt,25,CHEST,../../nbt/Chests/Rare3.nbt,25,CHEST,../../nbt/Chests/Rare4.nbt,25,CHEST,../../nbt/Chests/Rare5.nbt,25,CHEST,../../nbt/Chests/Rare6.nbt,25,CHEST,../../nbt/Chests/Rare7.nbt,25,CHEST,../../nbt/Chests/Rare8.nbt,25,CHEST,../../nbt/Chests/Rare9.nbt,25,CHEST,../../nbt/Chests/Rare10.nbt,25,CHEST,../../nbt/Chests/Rare11.nbt,25,CHEST,../../nbt/Chests/Rare12.nbt,25,CHEST,../../nbt/Chests/Rare13.nbt,25,CHEST,../../nbt/Chests/Rare14.nbt,25,CHEST,../../nbt/Chests/Rare15.nbt,100'
                                                                        elif str(chests[j]['Items'][0]['id']) == 'minecraft:diamond_block':
                                                                                mcid = 'CHEST,../../nbt/Chests/Epic1.nbt,25,CHEST,../../nbt/Chests/Epic2.nbt,25,CHEST,../../nbt/Chests/Epic3.nbt,25,CHEST,../../nbt/Chests/Epic4.nbt,25,CHEST,../../nbt/Chests/Epic5.nbt,25,CHEST,../../nbt/Chests/Epic6.nbt,25,CHEST,../../nbt/Chests/Epic7.nbt,25,CHEST,../../nbt/Chests/Epic8.nbt,25,CHEST,../../nbt/Chests/Epic9.nbt,25,CHEST,../../nbt/Chests/Epic10.nbt,25,CHEST,../../nbt/Chests/Epic11.nbt,25,CHEST,../../nbt/Chests/Epic12.nbt,25,CHEST,../../nbt/Chests/Epic13.nbt,25,CHEST,../../nbt/Chests/Epic14.nbt,25,CHEST,../../nbt/Chests/Epic15.nbt,100'
                                                                        else:
                                                                                mcid += chests[j].name+".nbt,100"
                                                                else:
                                                                        mcid += chests[j].name+".nbt,100"
                                                                        
                                                        else:
                                                                mcid += chests[j].name+".nbt,100"
                                elif mcid == '52':
                                        mcid = "MOB_SPAWNER,../../nbt/Spawner/"
                                        for j in range(len(spawners)):
                                                if x == spawners[j]['x'].value and z == spawners[j]['z'].value and y == spawners[j]['y'].value:
                                                        mcid += spawners[j].name+".nbt,100"
                                else:
                                        mcid += ",../../nbt/Misc/"
                                        for j in range(len(misc)):
                                                if x == misc[j]['x'].value and z == misc[j]['z'].value and y == misc[j]['y'].value:
                                                        mcid += misc[j].name+".nbt,100"
                        else:
                                line = "Block("
                                if data[i] != 0:
                                        mcid += ":"+str(data[i])
                        line += str(x%16-8)+","+str(y)+","+str(z%16-7)+","+mcid
                        line += ")\n"
                        if hasattr(outfile, 'read'):
                                outfile.write(line)
                        else:
                                outfile[int(x/16)][int(z/16)].write(line)

# Finish up bo3 files.
if hasattr(outfile, 'read'):
        for line in bo3template.bottom():
                outfile.write(line)
# Create branching structure if more than one file
else:
        for i in range(math.ceil(width/16)):
                for j in range(math.ceil(length/16)):
                        for line in bo3template.bottom():
                                outfile[i][j].write(line)
                        if j == 0 and i < math.ceil(width/16)-1:
                                outfile[i][j].write('Branch(16,0,0,'+name+'-C'+str(i+1)+'R0,NORTH,100)\n')
                        if j < math.ceil(length/16)-1:
                                outfile[i][j].write('Branch(0,0,16,'+name+'-C'+str(i)+'R'+str(j+1)+',NORTH,100)\n')
#y = i % height
#z = math.floor(i / height) % length
#x = math.floor(i / (height * length)) % width
