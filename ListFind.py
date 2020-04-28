# This script is designed to identify if files in a folder are part of a list, and duplicate them to another folder.

from shutil import copy
import os

filepath = "/srv/projects3/human_plasmids/georgina/"
outpath = "/srv/projects3/human_plasmids/georgina/ibdmdb-contigs_unzipped_unique/"


with open(filepath+"Unique-Sample-List.txt", "r") as f:
    uniqueList = [line.rstrip('\n') for line in f]
for file in os.listdir(filepath+"ibdmdb-contigs_unzipped3"):
    name = file.split('_c')[0]
    if name.strip("fr.") in uniqueList:
        print ("Found match for ", file)
        copy(filepath+"ibdmdb-contigs_unzipped3/"+file, outpath)
print ("Copy Complete.")





