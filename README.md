# NBTtobo3
Conversion tools for Terrain Control with Biome Bundle integration

Warning, this is currently spaghetti code at the moment.
It works as a means to an end, but it's not useable as a library.

## Requirements
 * [These all require Python 3.6 installed and appended to PATH](https://www.python.org/downloads/release/python-360/)
 * [They also use the NBT module made by Twoolie](https://github.com/twoolie/NBT) 
 
## Usage
### schematic2bo3.py
 1. Edit the 'template.txt' to your liking. The settings from this file will be set for all files processed with the script.
 2. You can double click on schematic2bo3.py or navigate to the file location in terminal/command prompt and run it with "python schematic2bo3.py"
 3. Select a .schematic file with the file browser
 4. The resulting bo3 file(s) and nbt folder tree will be output in a new folder in the source file directory.
 
 #### Notes
  * This program can handle large structures up to 10x10 chunks (160x160 blocks)
  * It also converts the tile entities in the .schematic to .nbt files that are easily merged with Biome Bundle's nbt folder structure.
   * If you place only a single iron, gold, or diamond block into a chest in the schematic beforehand, it will convert the chest to the Common, Rare, and Epic loot chest distribution from Biome Bundle

### nbt2bo3.py
 1. Open terminal/command prompt, navigate to the program location, and run it via "python nbt2bo3.py"
 2. Enter the directory with the nbt files. WARNING! This will attempt to convert all nbt files in the directory even if they are not the proper structure format.
 3. Enter the X and Y offset to be ADDED
 4. The resulting bo3 files(s) will be output in a new folder in the source file directory
 
### nbtadder.py
 1. Export a single (or double) chest via the Minecraft structure block and name it "itemlibrary"
 2. Copy the resulting itemlibrary.nbt from the Minecraft world/structures folder to the same folder as (I would recommend using a copy of) the Biome Bundle chests: Common, Rare, and Epic 1-15 and Trapped 1-8
 3. Copy nbtadder.py to the same directory you copied the files in the previous step to.
 4. Open terminal/command prompt and navigate the directory with all the files and run the program with "python nbtadder.py"
 5. The program will cycle through all the items in itemlibrary.nbt, print a pretty tree of the item so you can tell what it is, and ask how many chests (out of how many) you want to randomly distribute it to for each chest type.
 6. If you did everthing correctly, it will modify all the Biome Bundle chests with the random distribution you specified
 
 #### Notes
  * WARNING Janky as hell. If you mess up at all, you have to start all over.

## License
MIT License

Copyright (c) 2017 retrontology

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
