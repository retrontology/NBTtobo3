import nbt
import os
import sys
import convertmcid

newname = 'bo3'
xoff = 0
zoff = 0

# Grab files location
location = input('Enter the directory of the .nbt files: ')

# Grab offsets
xoff = int(input('Enter X Offset: '))
zoff = int(input('Enter Z Offset: '))

# Open all nbt files
nbtfiles = []
for file in os.listdir(location):
    if(file.endswith(".nbt")):
        nbtfiles.append(file)
		
# Make new directory for new files (if there are any)
if nbtfiles:
    newlocation = '%s' % location + "\\" + newname
    if not os.path.isdir(newlocation):
        os.mkdir(newlocation)

# Meat n Potatos
for file in nbtfiles:
	# Set up Palette
	nbtee = nbt.nbt.NBTFile(location + "\\" + file)
	pal = []
	for tag in nbtee['palette']:
		pal.append(convertmcid.convertNBTToBlock(tag))
	
	# Grab templates
	template = open('template.txt', 'r')
	
	# Make bo3 file
	outfile = open(newlocation + "\\" + file.replace('.nbt', '.bo3'), 'w')	
	
	# Write top half of template
	for line in template:
		outfile.write(line)
		if line == '#  spawns the bottom part of an igloo.\n':
			break
	
	# Write blocks to file
	print(newlocation + "\\" + file.replace('.nbt', '.bo3'))
	
	for tag in nbtee['blocks']:
		item = pal[tag.__getitem__('state').value]
		if item[:item.find(':')] == 'CHEST' or item == 'MOB_SPAWNER':
			block = 'RandomBlock('
		else:
			block = 'Block('
		block = block + str(tag['pos'][0].value+xoff) + ',' + str(tag['pos'][1].value) + ',' + str(tag['pos'][2].value+zoff) + ',' + pal[tag.__getitem__('state').value] +')'
		outfile.write(block + '\n')
	
	# Write bottom half of template
	for line in template:
		outfile.write(line)