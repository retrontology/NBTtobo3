name = 'template.txt'

def top():
    # Import template
    template = open(name, 'r')
    # Write top half of template
    lines = []
    for line in template:
        lines.append(line)
        if line == '#  spawns the bottom part of an igloo.\n':
            break
    return lines

def bottom():
    # Import template
    template = open(name, 'r')
    # Cycle through file to bottom half
    for line in template:
        if line == '#  spawns the bottom part of an igloo.\n':
            break
    # Write bottom half of template
    lines = []
    for line in template:
        lines.append(line)
    return lines
