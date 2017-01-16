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
tiletemp = ['54', '52', '138', '137']
bbchest = True

# Make sure schematic is small enough
assert length <= 160 and width <= 160, name + ".schematic is too large to convert to bo3. bo3 files can only handle structure dimensions up to 160x160 blocks (10x10 chunks)"

# Create nbt files from schematic
nbtlocation = outlocation + os.sep + 'nbt'
chestlocation = nbtlocation + os.sep + 'Chests'
spawnerlocation = nbtlocation + os.sep + 'Spawner'
misclocation = nbtlocation + os.sep + 'Misc'
if schematic['TileEntities']:
        print("Creating nbt files...")
# Create a counter dictionary to record how many of each type we have for names
# Better than checking the list each time which results in O*!N (I think?)
class Counter(dict):
        def __missing__(self, key):
                return 0
tiles = Counter()
tileent = []
# Cycle through tile entities to create nbt files and add them to a list for name/coord storage
for ent in schematic['TileEntities']:
        # Create Directory if it doesn't exist
        if not os.path.isdir(nbtlocation):
                os.mkdir(nbtlocation)
        # Create name for file
        file = nbt.NBTFile()
        file.name = name + "-" + str(ent['id'])[str(ent['id']).find(':')+1:].title()
        tiles[str(ent['id'])] += 1
        file.name += str(tiles[str(ent['id'])])
        # Append all tags but x,y,z
        for i in range(len(ent)):
                # The below line in comment only filters out x,y,z and not the World Edit stuff
                #if not (ent[i].name == 'x' or ent[i].name == 'y' or ent[i].name == 'z'):
                if not isinstance(ent[i], nbt.TAG_Int):
                        file.tags.append(ent[i])
        # Write File
        if str(ent['id']) == 'minecraft:chest' or str(ent['id']) == 'minecraft:trapped_chest':
                if not os.path.isdir(chestlocation):
                        os.mkdir(chestlocation)
                file.write_file(chestlocation+os.sep+file.name+".nbt")
        elif str(ent['id']) == 'minecraft:mob_spawner':
                if not os.path.isdir(spawnerlocation):
                        os.mkdir(spawnerlocation)
                file.write_file(spawnerlocation+os.sep+file.name+".nbt")
        else:
                if not os.path.isdir(misclocation):
                        os.mkdir(misclocation)
                file.write_file(misclocation+os.sep+file.name+".nbt")
        # Add coords and append to list for future reference in bo3 building
        file.tags.append(ent['x'])
        file.tags.append(ent['y'])
        file.tags.append(ent['z'])
        tileent.append(file)

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
                        line = 'Block('
                        mcid = str(blocks[i])
                        if data[i] != 0:
                                mcid += ':' + str(data[i])
                        # change mcid and line if block is a tileent
                        for ent in tileent:
                                if x == ent['x'].value and y == ent['y'].value and z == ent['z'].value:
                                        line = 'RandomBlock('
                                        if str(ent['id']) == 'minecraft:chest':
                                                if bbchest and len(ent['Items']) == 1:
                                                        if str(ent['Items'][0]['id']) == 'minecraft:iron_block':
                                                                mcid = 'CHEST,../../nbt/Chests/Common1.nbt,25,CHEST,../../nbt/Chests/Common2.nbt,25,CHEST,../../nbt/Chests/Common3.nbt,25,CHEST,../../nbt/Chests/Common4.nbt,25,CHEST,../../nbt/Chests/Common5.nbt,25,CHEST,../../nbt/Chests/Common6.nbt,25,CHEST,../../nbt/Chests/Common7.nbt,25,CHEST,../../nbt/Chests/Common8.nbt,25,CHEST,../../nbt/Chests/Common9.nbt,25,CHEST,../../nbt/Chests/Common10.nbt,25,CHEST,../../nbt/Chests/Common11.nbt,25,CHEST,../../nbt/Chests/Common12.nbt,25,CHEST,../../nbt/Chests/Common13.nbt,25,CHEST,../../nbt/Chests/Common14.nbt,25,CHEST,../../nbt/Chests/Common15.nbt,100'
                                                        elif str(ent['Items'][0]['id']) == 'minecraft:gold_block':
                                                                mcid = 'CHEST,../../nbt/Chests/Rare1.nbt,25,CHEST,../../nbt/Chests/Rare2.nbt,25,CHEST,../../nbt/Chests/Rare3.nbt,25,CHEST,../../nbt/Chests/Rare4.nbt,25,CHEST,../../nbt/Chests/Rare5.nbt,25,CHEST,../../nbt/Chests/Rare6.nbt,25,CHEST,../../nbt/Chests/Rare7.nbt,25,CHEST,../../nbt/Chests/Rare8.nbt,25,CHEST,../../nbt/Chests/Rare9.nbt,25,CHEST,../../nbt/Chests/Rare10.nbt,25,CHEST,../../nbt/Chests/Rare11.nbt,25,CHEST,../../nbt/Chests/Rare12.nbt,25,CHEST,../../nbt/Chests/Rare13.nbt,25,CHEST,../../nbt/Chests/Rare14.nbt,25,CHEST,../../nbt/Chests/Rare15.nbt,100'
                                                        elif str(ent['Items'][0]['id']) == 'minecraft:diamond_block':
                                                                mcid = 'CHEST,../../nbt/Chests/Epic1.nbt,25,CHEST,../../nbt/Chests/Epic2.nbt,25,CHEST,../../nbt/Chests/Epic3.nbt,25,CHEST,../../nbt/Chests/Epic4.nbt,25,CHEST,../../nbt/Chests/Epic5.nbt,25,CHEST,../../nbt/Chests/Epic6.nbt,25,CHEST,../../nbt/Chests/Epic7.nbt,25,CHEST,../../nbt/Chests/Epic8.nbt,25,CHEST,../../nbt/Chests/Epic9.nbt,25,CHEST,../../nbt/Chests/Epic10.nbt,25,CHEST,../../nbt/Chests/Epic11.nbt,25,CHEST,../../nbt/Chests/Epic12.nbt,25,CHEST,../../nbt/Chests/Epic13.nbt,25,CHEST,../../nbt/Chests/Epic14.nbt,25,CHEST,../../nbt/Chests/Epic15.nbt,100'
                                                else:
                                                        mcid = 'CHEST,../../nbt/Chests/' + ent.name + '.nbt,100'
                                        elif str(ent['id']) == 'minecraft:trapped_chest':
                                                if bbchest:
                                                        mcid = 'TRAPPED_CHEST,../../nbt/Chests/TrappedChest1.nbt,25,TRAPPED_CHEST,../../nbt/Chests/TrappedChest2.nbt,25,TRAPPED_CHEST,../../nbt/Chests/TrappedChest3.nbt,25,TRAPPED_CHEST,../../nbt/Chests/TrappedChest4.nbt,25,TRAPPED_CHEST,../../nbt/Chests/TrappedChest5.nbt,25,TRAPPED_CHEST,../../nbt/Chests/TrappedChest6.nbt,25,TRAPPED_CHEST,../../nbt/Chests/TrappedChest7.nbt,25,TRAPPED_CHEST,../../nbt/Chests/TrappedChest8.nbt,100'
                                                else:
                                                        mcid = 'TRAPPED_CHEST,../../nbt/Chests/' + ent.name + '.nbt,100'
                                        elif str(ent['id']) == 'minecraft:mob_spawner':
                                                mcid = 'MOB_SPAWNER,../../nbt/Spawner/' + ent.name  + '.nbt,100'
                                        else:
                                                mcid += ',../../nbt/Misc/' + ent.name  + '.nbt,100'
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
