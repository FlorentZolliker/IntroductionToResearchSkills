# Simple read file for the coordinate input
# 
# to use, either import the function with: from readCoord import readCoord
# or use directly the function definition in your project
#
# example usage: e,n,h  = readCoord("In_WGS84_lab1-2021.txt")
# you will need to convert the string to float with float()



def readCoord(file_name):
    '''
    Simple read file for the coordinate input.
    
    To use, either import the function with: from readCoord import readCoord or use directly the function definition in your project.

    Example usage: e,n,h  = readCoord("In_WGS84_lab1-2021.txt")
    You will need to convert the string to float with float()
    '''
    for line in open(file_name):
        li=line.strip()
        if not li.startswith("#") and li != "\n":
            print("Coordinates: "  + line.rstrip())
            my_coor = line.rstrip().split()
    return my_coor
