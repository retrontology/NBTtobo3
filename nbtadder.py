import nbt
import random

def randomSequence(prob, length):
    "This generates a random sequence of identical numbers with a length specified by the parameter"
    sequence = []
    for i in range(length):
        sequence.append(i)
    random.shuffle(sequence)
    for i in range(length - prob):
        del sequence[-1]
    return sequence

def addShuffle(nchest, tag, prob, length):
    array_prob = randomSequence(prob, length)
    for marker in array_prob:
        chest = nchest[marker]["Items"]
        slot = nbt.nbt.TAG_Byte(random.randrange(27))
        for i in range(0, chest.__len__()):
            if chest[i]["Slot"].value == slot:
                del chest[i]
                break
        chest.append(tag)
        chest[-1]["Slot"] = slot

librarynbt = nbt.nbt.NBTFile("itemlibrary.nbt")
libitem = librarynbt["blocks"][0]["nbt"]["Items"]
itempart2= librarynbt["blocks"][1]["nbt"]["Items"]
for tag in itempart2:
    libitem.append(tag)
    
common = []
rare = []
epic = []
trapped = []
for i in range(1,16):
    common.append(nbt.nbt.NBTFile("Common"+str(i)+".nbt"))
    rare.append(nbt.nbt.NBTFile("Rare"+str(i)+".nbt"))
    epic.append(nbt.nbt.NBTFile("Epic"+str(i)+".nbt"))
for i in range(1,9):
    trapped.append(nbt.nbt.NBTFile("TrappedChest"+str(i)+".nbt"))

for tag in libitem:
    print(tag.pretty_tree())
    prob_common = int(input('Common #/15: '))
    prob_rare = int(input('Rare #/15: '))
    prob_epic = int(input('Epic #/15: '))
    prob_trapped = int(input('Trapped #/8: '))
    
    addShuffle(common, tag, prob_common, 15)
    addShuffle(rare, tag, prob_rare, 15)
    addShuffle(epic, tag, prob_epic, 15)
    addShuffle(trapped, tag, prob_trapped, 8)

for i in range(1,16):
    common[i-1].write_file("Common"+str(i)+".nbt")
    rare[i-1].write_file("Rare"+str(i)+".nbt")
    epic[i-1].write_file("Epic"+str(i)+".nbt")
    
for i in range(1,9):
    trapped[i-1].write_file("TrappedChest"+str(i)+".nbt")
