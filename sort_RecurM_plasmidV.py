# This code takes in the output of RecurM and reformats it into a multifasta for input into plasmidVerify.py

#!/usr/bin/env python3

import csv
import os.path
from datetime import date
from Bio import SeqIO

today = date.today()

# Set the input location
in_path = "/srv/home/s4479877/python/RecurM_v2/Test3_output"
# Set the output location
out_path = "/srv/home/s4479877/python/RecurM_Sort/"
# Take in a list of the RecurM output clusters

cluster_folders = os.listdir(in_path)
plasmids = ""
# Open Folder
for folder in cluster_folders:
    print("Reading folder ", folder)
    cluster = list(SeqIO.parse("{}/{}/{}".format(in_path, folder, "cluster_out.fa"), "fasta"))
    repseq = cluster[0].seq
    repseqid = cluster[0].id
    plasmids += ">"+str(repseqid)+"\n"+str(repseq)+"\n"

output = open(out_path+"potential_plasmids.fna","w")
output.write(plasmids)
output.close()
